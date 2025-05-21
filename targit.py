import os
import tarfile
from gitignore_parser import parse_gitignore
import argparse

def create_tarball_respecting_gitignore(output_filename, source_dir='.'):
    """
    Creates a .tar.gz archive of the source_dir, excluding files and
    directories specified in the .gitignore file found in source_dir.

    Args:
        output_filename (str): The name of the .tar.gz file to create.
        source_dir (str): The directory to archive. Defaults to the current directory.
    """
    gitignore_path = os.path.join(source_dir, '.gitignore')
    matches = None
    if os.path.exists(gitignore_path):
        matches = parse_gitignore(gitignore_path, base_dir=os.path.abspath(source_dir))
    else:
        print(f"Warning: No .gitignore file found in {source_dir}. Archiving all files.")

    # Ensure the output filename ends with .tar.gz
    if not output_filename.endswith(".tar.gz"):
        output_filename += ".tar.gz"

    print(f"Creating archive: {output_filename} from directory: {source_dir}")

    with tarfile.open(output_filename, "w:gz") as tar:
        for root, dirs, files in os.walk(source_dir, topdown=True):
            # --- .gitignore logic for directories ---
            # Filter directories in place so os.walk doesn't traverse them
            # We need to check the absolute path for directories
            original_dirs_len = len(dirs)
            dirs[:] = [
                d for d in dirs
                if not (
                    d == os.path.basename(output_filename) and root == source_dir # Don't include the tarball itself
                    or (matches and matches(os.path.abspath(os.path.join(root, d))))
                )
            ]
            if len(dirs) < original_dirs_len:
                print(f"Ignoring directories in {root} based on .gitignore: {[d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)) and d not in dirs]}")


            for file_name in files:
                if file_name == os.path.basename(output_filename) and root == source_dir:
                    continue # Don't include the tarball itself

                file_path = os.path.join(root, file_name)
                abs_file_path = os.path.abspath(file_path)

                if matches and matches(abs_file_path):
                    print(f"Ignoring file: {file_path}")
                    continue

                # Add file to tar, using a relative path within the archive
                # os.path.relpath is important for correct structure in the tarball
                arcname = os.path.relpath(file_path, source_dir)
                print(f"Adding: {file_path} as {arcname}")
                tar.add(file_path, arcname=arcname)
    print(f"Successfully created {output_filename}")

if __name__ == '__main__':
    # --- How to use it ---
    parser = argparse.ArgumentParser(description="Create a .tar.gz archive while respecting .gitignore.")
    parser.add_argument('output_filename', type=str, help='Output .tar.gz filename')
    parser.add_argument('source_dir', type=str, nargs='?', default='.', help='Source directory to archive (default: current directory)')
    args = parser.parse_args()
    project_directory = args.source
    output_archive_name = args.output

    # Create a dummy .gitignore for testing if you don't have one
    if not os.path.exists(os.path.join(project_directory, '.gitignore')):
        with open(os.path.join(project_directory, '.gitignore'), 'w') as f:
            f.write("*.log\n")
            f.write("*.tmp\n")
            f.write("dist/\n")
            f.write("__pycache__/\n")
            f.write(".DS_Store\n")
            f.write("*.swo\n")
            f.write("*.swp\n")
            f.write("my_project_archive.tar.gz\n") # Ignore the output archive itself
        print("Created a dummy .gitignore file for demonstration.")

    # Create some dummy files and directories for testing
    if not os.path.exists("dist"):
        os.makedirs("dist")
    if not os.path.exists("__pycache__"):
        os.makedirs("__pycache__")
    open("main.py", "w").close()
    open("data.txt", "w").close()
    open("app.log", "w").close()
    open("dist/output.exe", "w").close()
    open("__pycache__/cache_file.pyc", "w").close()


    create_tarball_respecting_gitignore(output_archive_name, project_directory)

    # --- To verify the contents (optional) ---
    # print(f"\nContents of '{output_archive_name}':")
    # with tarfile.open(output_archive_name, "r:gz") as tar:
    #     for member in tar.getmembers():
    #         print(member.name)
