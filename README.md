# targit

A Python utility to create a `.tar.gz` archive of your project directory, automatically respecting your `.gitignore` rules. This helps you package your project while excluding files and directories you don't want to share or deploy.

## Features

- Archives your project directory into a `.tar.gz` file.
- Excludes files and directories listed in your `.gitignore`.
- Prevents the archive from including itself.
- Simple to use and extend.

## Requirements

- Python 3.6+
- [`gitignore_parser`](https://pypi.org/project/gitignore-parser/)

Install the required dependency with:

```bash
pip install gitignore_parser
```

## Usage

Run the script directly:

```bash
python targit.py
```

By default, this will:

- Create a `.gitignore` file if one does not exist (for demonstration).
- Create some dummy files and directories.
- Archive the current directory into `my_project_archive.tar.gz`, excluding files/directories matched by `.gitignore`.

You can customize the source directory and output filename by modifying these lines in `targit.py`:

```python
project_directory = '.'  # Change to your project root if needed
output_archive_name = 'my_project_archive.tar.gz'
```

## Example

After running:

```bash
python targit.py
```

You will see output indicating which files are added or ignored, and a `my_project_archive.tar.gz` file will be created in your directory.

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

## License

MIT License

---

*Created with ❤️ for reproducible Python packaging!*