
# CodeSpoonFeeder

CodeSpoonFeeder is a Flask-based web application designed to help users quickly and easily organize, structure, and download large project directories as compressed files. Upload a project folder, select specific files, and get a well-structured output with streamlined code segments. Perfect for developers and project managers looking to easily share, inspect, and analyze codebases!

## Features
- Upload project directories or zip files up to 500 MB.
- Generate structured overviews of file contents.
- Download segmented text files to inspect or share easily.
- Automatic deletion of old directories to manage storage efficiently.

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:
- **Python 3.12** (Other Python 3 versions may work but are not guaranteed)
- **Flask** and other dependencies (installation steps below)

### Installation

1. **Clone the repository** to your local machine.

   ```bash
   git clone git@github.com:yipy0005/codespoonfeeder.git
   cd codespoonfeeder
   ```

2. **Set up the environment**. We recommend using `conda` to manage dependencies.

   ```bash
   conda env create -f environment.yaml
   conda activate codespoonfeeder
   ```

3. **Configure environment variables** (optional):
   - Set up the `SECRET_KEY` environment variable for session management.

4. **Run the Flask app**.

   ```bash
   python app.py
   ```

   The app should be running at `http://localhost:5001`.

5. **Open your browser** and navigate to `http://localhost:5001` to start using CodeSpoonFeeder.

## Usage

1. **Upload a Directory**: Navigate to the homepage and upload your project directory or a zip file of your project.
2. **Select Files**: Choose specific files or folders you want to process.
3. **Download Output**: Get a zip file containing structured, segmented text files of your selected code.

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

Feel free to reach out through GitHub issues if you encounter any bugs or have suggestions for improvements.
