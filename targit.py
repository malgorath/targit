
"""
targit.py

Creates a .tar.gz archive of a project directory, excluding files and directories specified in .gitignore.

Usage:
    python targit.py <output_filename> [source_dir]

Requirements:
    - Python 3.6+
    - gitignore_parser (install via pip)

Author: malgorath
License: MIT
"""

import os
import tarfile
from gitignore_parser import parse_gitignore
import argparse


def create_tarball_respecting_gitignore(output_filename, source_dir='.'):
    """
    Create a .tar.gz archive of the source_dir, excluding files and directories specified in .gitignore.

    Args:
        output_filename (str): Name of the output .tar.gz file.
        source_dir (str): Directory to archive. Defaults to current directory.

    Returns:
        None
    """
    gitignore_path = os.path.join(source_dir, '.gitignore')
    matches = None
    if os.path.exists(gitignore_path):
        # Parse .gitignore rules
        matches = parse_gitignore(gitignore_path, base_dir=os.path.abspath(source_dir))
    else:
        print(f"Warning: No .gitignore file found in {source_dir}. Archiving all files.")

    # Ensure output filename ends with .tar.gz
    if not output_filename.endswith(".tar.gz"):
        output_filename += ".tar.gz"

    print(f"Creating archive: {output_filename} from directory: {source_dir}")

    with tarfile.open(output_filename, "w:gz") as tar:
        for root, dirs, files in os.walk(source_dir, topdown=True):
            # Filter directories in place so os.walk doesn't traverse ignored ones
            original_dirs_len = len(dirs)
            dirs[:] = [
                d for d in dirs
                if not (
                    d == os.path.basename(output_filename) and root == source_dir  # Don't include the tarball itself
                    or (matches and matches(os.path.abspath(os.path.join(root, d))))
                )
            ]
            if len(dirs) < original_dirs_len:
                ignored_dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and d not in dirs]
                print(f"Ignoring directories in {root} based on .gitignore: {ignored_dirs}")

            for file_name in files:
                # Skip the output archive itself
                if file_name == os.path.basename(output_filename) and root == source_dir:
                    continue

                file_path = os.path.join(root, file_name)
                abs_file_path = os.path.abspath(file_path)

                # Skip files matching .gitignore
                if matches and matches(abs_file_path):
                    print(f"Ignoring file: {file_path}")
                    continue

                # Add file to tar, using relative path for correct structure
                arcname = os.path.relpath(file_path, source_dir)
                print(f"Adding: {file_path} as {arcname}")
                tar.add(file_path, arcname=arcname)
    print(f"Successfully created {output_filename}")


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Create a .tar.gz archive while respecting .gitignore."
    )
    parser.add_argument('output_filename', type=str, help='Output .tar.gz filename')
    parser.add_argument('source_dir', type=str, nargs='?', default='.', help='Source directory to archive (default: current directory)')
    args = parser.parse_args()

    project_directory = args.source_dir
    output_archive_name = args.output_filename

    # Create a dummy .gitignore for demonstration if not present
    if not os.path.exists(os.path.join(project_directory, '.gitignore')):
        with open(os.path.join(project_directory, '.gitignore'), 'w') as f:
            f.write("*.log\n")
            f.write("*.tmp\n")
            f.write("dist/\n")
            f.write("__pycache__/\n")
            f.write(".DS_Store\n")
            f.write("*.swo\n")
            f.write("*.swp\n")
            f.write(f"{output_archive_name}\n") # Ignore the output archive itself
        print("Created a dummy .gitignore file for demonstration.")

    # Create some dummy files and directories for demonstration
    for d in ["dist", "__pycache__"]:
        if not os.path.exists(d):
            os.makedirs(d)
    for fname in ["main.py", "data.txt", "app.log", "dist/output.exe", "__pycache__/cache_file.pyc"]:
        dir_name = os.path.dirname(fname)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        open(fname, "w").close()

    # Create the archive
    create_tarball_respecting_gitignore(output_archive_name, project_directory)

    # Optional: Print contents of the archive
    # print(f"\nContents of '{output_archive_name}':")
    # with tarfile.open(output_archive_name, "r:gz") as tar:
    #     for member in tar.getmembers():
    #         print(member.name)
