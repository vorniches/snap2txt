import os
import sys
import argparse

def read_list_file(file_path):
    """
    Read a list file (.il or .wl) and return the list of patterns.

    :param file_path: Path to the list file.
    :return: A list of patterns.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"List file not found: {file_path}")
        return []

def match_pattern(path, patterns):
    """
    Check if a given path matches any of the patterns in the list.

    :param path: The file or directory path.
    :param patterns: A list of patterns to match against.
    :return: True if path matches any pattern, False otherwise.
    """
    for pattern in patterns:
        if pattern in path:
            return True
    return False

def save_project_structure_and_files(root_path, output_file, ignore_list=None, whitelist=None):
    """
    Save the project structure and contents of all files in the project to a text file,
    considering ignore and whitelist.

    :param root_path: Root directory of the project.
    :param output_file: Path to the output text file.
    :param ignore_list: List of patterns to ignore.
    :param whitelist: List of patterns to include.
    """
    project_structure = []
    file_contents = []

    for root, dirs, files in os.walk(root_path):
        # Filter directories and files based on ignore_list and whitelist
        dirs[:] = [d for d in dirs if not match_pattern(d, ignore_list or []) and (not whitelist or match_pattern(d, whitelist))]
        files = [f for f in files if not match_pattern(f, ignore_list or []) and (not whitelist or match_pattern(f, whitelist))]

        for file in files:
            rel_dir = os.path.relpath(root, root_path)
            rel_file = os.path.join(rel_dir, file)
            project_structure.append(rel_file.replace("\\", "/"))

            try:
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                file_contents.append(f"{file}:\n```\n{content}\n```\n")
            except Exception as e:
                file_contents.append(f"{file}:\n```\nError reading file: {e}\n```\n")

    with open(output_file, 'w') as f:
        f.write("Project Structure:\n")
        f.write("\n".join(project_structure) + "\n\n")
        f.write("File Contents:\n")
        f.write("\n".join(file_contents))

def main():
    script_dir = os.path.dirname(__file__)  # Get the directory where the script is located
    il_file = os.path.join(script_dir, '.il')  # Path to .il file
    wl_file = os.path.join(script_dir, '.wl')  # Path to .wl file

    parser = argparse.ArgumentParser(description="Save project structure and file contents.")
    parser.add_argument("--il", help="Use ignore list (.il file)", action="store_true")
    parser.add_argument("--wl", help="Use whitelist (.wl file)", action="store_true")
    args = parser.parse_args()

    ignore_list = read_list_file(il_file) if args.il else None
    whitelist = read_list_file(wl_file) if args.wl else None

    save_project_structure_and_files('.', 'project_contents.txt', ignore_list, whitelist)

if __name__ == "__main__":
    main()
