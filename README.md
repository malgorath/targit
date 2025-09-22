
# targit

**targit** is a Python utility to create a `.tar.gz` archive of your project directory, automatically respecting your `.gitignore` rules. This helps you package your project while excluding files and directories you don't want to share or deploy.

## Features

- Archives your project directory into a `.tar.gz` file
- Excludes files and directories listed in your `.gitignore`
- Prevents the archive from including itself
- Simple CLI usage

## Requirements

- Python 3.6+
- [`gitignore_parser`](https://pypi.org/project/gitignore-parser/)

Install the required dependency:

```bash
pip install gitignore_parser
```

## Usage

Run the script from the command line:

```bash
python targit.py <output_filename> [source_dir]
```

- `output_filename`: Name of the output archive (e.g. `my_project_archive.tar.gz`)
- `source_dir`: Directory to archive (defaults to current directory)

Example:

```bash
python targit.py my_project_archive.tar.gz .
```

The script will:

- Create a `.gitignore` file if one does not exist (for demonstration)
- Create some dummy files and directories (for demonstration)
- Archive the specified directory, excluding files/directories matched by `.gitignore`

## Customizing `.gitignore`

Edit the `.gitignore` file in your project root to specify which files or directories to exclude from the archive. Example:

```
*.log
*.tmp
dist/
__pycache__/
.DS_Store
*.swo
*.swp
my_project_archive.tar.gz
```

## Output

You will see output indicating which files are added or ignored, and a `.tar.gz` file will be created in your directory.


## Building a Standalone Binary

This project includes a `Makefile` to easily build a standalone binary using PyInstaller.

### Compile the Binary

First, ensure you have PyInstaller installed:

```bash
pip install pyinstaller
```

Then run:

```bash
make
```

This will create a binary named `targit` in the `dist/` directory.

### Install the Binary System-wide

To move the binary to `/usr/local/bin` (requires sudo):

```bash
sudo mv dist/targit /usr/local/bin/targit
```

You can now run `targit` from anywhere:

```bash
targit <output_filename> [source_dir]
```

### Clean Build Artifacts

To remove build files:

```bash
make clean
```

## License

MIT License

---

*Created with ❤️ for reproducible Python packaging!*