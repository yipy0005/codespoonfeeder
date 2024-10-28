from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import zipfile
import io
import uuid
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB
app.config['MAX_FORM_MEMORY_SIZE'] = 500 * 1024 * 1024  # 500 MB


@app.before_request
def log_request_info():
    print('Request Headers: %s', request.headers)
    print('Content Length: %s', request.content_length)

def stream_factory(total_content_length, content_type, filename, content_length=None):
    temp_file = tempfile.NamedTemporaryFile('wb+', delete=False)
    return temp_file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    request.stream_factory = stream_factory
    if 'project_folder' not in request.files:
        return "No file part"
    files = request.files.getlist('project_folder')
    session_id = str(uuid.uuid4())
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(save_path, exist_ok=True)

    for file in files:
        filename = file.filename
        file_path = os.path.join(save_path, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

    return redirect(url_for('select_files', session_id=session_id))

@app.route('/select_files/<session_id>')
def select_files(session_id):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    file_structure = get_file_structure(user_folder, user_folder)
    return render_template('select_files.html', file_structure=file_structure, session_id=session_id)

def get_file_structure(root_folder, current_folder):
    file_structure = []
    for item in os.listdir(current_folder):
        item_path = os.path.join(current_folder, item)
        relative_path = os.path.relpath(item_path, root_folder)
        if os.path.isdir(item_path):
            file_structure.append({
                'type': 'folder',
                'name': item,
                'path': relative_path,
                'children': get_file_structure(root_folder, item_path)
            })
        else:
            file_structure.append({
                'type': 'file',
                'name': item,
                'path': relative_path
            })
    return file_structure

@app.route('/process_files/<session_id>', methods=['POST'])
def process_files(session_id):
    selected_paths = request.form.getlist('selected_paths')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    combined_text = ''

    for relative_path in selected_paths:
        file_path = os.path.join(user_folder, relative_path)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    combined_text += f.read() + '\n'
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    segments = split_text_by_words(combined_text, 5000)

    output_folder = os.path.join(user_folder, 'output')
    os.makedirs(output_folder, exist_ok=True)
    segment_files = []
    for i, segment in enumerate(segments):
        segment_filename = f'output_part_{i+1}.txt'
        segment_path = os.path.join(output_folder, segment_filename)
        with open(segment_path, 'w', encoding='utf-8') as f:
            f.write(segment)
        segment_files.append(segment_path)

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file_path in segment_files:
            zf.write(file_path, os.path.basename(file_path))
    memory_file.seek(0)

    # Updated line using download_name instead of attachment_filename
    return send_file(memory_file, download_name='output_segments.zip', as_attachment=True)


def split_text_by_words(text, word_limit):
    words = text.split()
    segments = []
    for i in range(0, len(words), word_limit):
        segment = ' '.join(words[i:i + word_limit])
        segments.append(segment)
    return segments


@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    file = request.files.get('project_zip')
    if file:
        session_id = str(uuid.uuid4())
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, 'project.zip')
        file.save(file_path)

        # Unzip the file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(save_path)

        # Remove the ZIP file if desired
        os.remove(file_path)

        return redirect(url_for('select_files', session_id=session_id))
    else:
        return "No file uploaded", 400


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(error):
    return "File is too large. Please upload a file smaller than 100 MB.", 413

if __name__ == '__main__':
    app.run(debug=True)
