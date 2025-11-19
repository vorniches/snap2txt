import os
import sys
import argparse
import fnmatch

def read_list_file(file_path):
    """
    Read a list file (.il or .wl) and return the list of patterns.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"List file not found: {file_path}")
        return []

def match_pattern(path, patterns, is_dir=False):
    """
    Check if a given path matches any of the patterns in the list.
    Supports:
    - Folder patterns ending with / (e.g., "node_modules/")
    - File extension patterns (e.g., "*.css", ".jpg")
    - Wildcards (e.g., "test*.js")
    - Full path patterns (e.g., "lib/realtime-client.ts")
    - Exact names (e.g., "package.json")
    - Substring patterns (e.g., "__pycache__")
    """
    if not patterns:
        return False
    
    # Normalize path separators
    path = path.replace("\\", "/")
    path_parts = path.split("/")
    basename = os.path.basename(path)
    
    for pattern in patterns:
        # Normalize pattern
        pattern = pattern.replace("\\", "/")
        
        # Pattern for directories (ends with /)
        if pattern.endswith("/"):
            dir_pattern = pattern.rstrip("/")
            if is_dir:
                # Check if any part of the path matches the directory name
                if dir_pattern in path_parts or basename == dir_pattern:
                    return True
            else:
                # For files, check if any parent directory matches
                if dir_pattern in path_parts:
                    return True
        
        # Pattern for file extensions (e.g., ".css", "*.css")
        elif pattern.startswith("*."):
            ext = pattern[1:]  # Remove the *
            if basename.endswith(ext):
                return True
        
        elif pattern.startswith(".") and not pattern.startswith("./"):
            # Extension pattern like ".css"
            if basename.endswith(pattern):
                return True
        
        # Wildcard pattern (e.g., "test*.js")
        elif "*" in pattern:
            if fnmatch.fnmatch(basename, pattern):
                return True
        
        # Full path match (e.g., "lib/realtime-client.ts")
        elif "/" in pattern:
            if pattern == path or path.endswith("/" + pattern):
                return True
        
        # Exact basename match
        elif pattern == basename:
            return True
        
        # Substring match in path parts (for patterns like "__pycache__")
        elif pattern in path_parts:
            return True
    
    return False

def should_include_path(path, is_dir, ignore_list, whitelist, whitelist_mode):
    """
    Determine if a path should be included based on ignore list and whitelist.
    
    Args:
        path: The file or directory path
        is_dir: Whether the path is a directory
        ignore_list: List of patterns to ignore
        whitelist: List of patterns to include
        whitelist_mode: If True, ONLY include whitelisted items (ignore ignore_list)
    
    Returns:
        True if the path should be included, False otherwise
    """
    if whitelist_mode:
        # In whitelist mode, ONLY include items that match the whitelist
        return match_pattern(path, whitelist, is_dir)
    else:
        # In normal mode, include everything except ignored items
        # If whitelist exists in non-whitelist mode, it acts as an additional filter
        if ignore_list and match_pattern(path, ignore_list, is_dir):
            return False
        if whitelist and not match_pattern(path, whitelist, is_dir):
            return False
        return True

def save_project_structure_and_files(root_path, output_file, ignore_list=None, whitelist=None, whitelist_mode=False):
    """
    Save the project structure and contents of all files in the project to a text file,
    considering ignore and whitelist.
    
    Args:
        root_path: The root directory to scan
        output_file: The output file path
        ignore_list: List of patterns to ignore
        whitelist: List of patterns to include
        whitelist_mode: If True, ONLY include whitelisted items (ignore ignore_list)
    """
    project_structure = []
    file_contents = []

    for root, dirs, files in os.walk(root_path):
        rel_dir = os.path.relpath(root, root_path)
        
        # Filter directories
        # In whitelist mode, traverse all directories but only filter files
        # In normal mode, filter directories to avoid traversing ignored ones
        if not whitelist_mode:
            filtered_dirs = []
            for d in dirs:
                dir_path = os.path.join(rel_dir, d) if rel_dir != "." else d
                if should_include_path(dir_path, True, ignore_list, whitelist, whitelist_mode):
                    filtered_dirs.append(d)
            dirs[:] = filtered_dirs
        
        # Filter and process files
        for file in files:
            file_path = os.path.join(rel_dir, file) if rel_dir != "." else file
            
            if should_include_path(file_path, False, ignore_list, whitelist, whitelist_mode):
                rel_file = file_path.replace("\\", "/")
                project_structure.append(rel_file)

                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_contents.append(f"{file}:\n```\n{content}\n```\n")
                except Exception as e:
                    file_contents.append(f"{file}:\n```\nError reading file: {e}\n```\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Project Structure:\n")
        f.write("\n".join(project_structure) + "\n\n")
        f.write("File Contents:\n")
        f.write("\n".join(file_contents))
    
    print(f"Project contents saved to {output_file}")
    print(f"Total files collected: {len(project_structure)}")

def main():
    script_dir = os.path.dirname(__file__)
    il_file = os.path.join(script_dir, '.il')
    wl_file = os.path.join(script_dir, '.wl')

    parser = argparse.ArgumentParser(description="Save project structure and file contents.")
    parser.add_argument("--il", help="Use ignore list (.il file)", action="store_true")
    parser.add_argument("--wl", help="Use whitelist (.wl file) - ONLY collect whitelisted items", action="store_true")
    parser.add_argument("--show-locations", help="Show the location of the .il and .wl files", action="store_true")

    args = parser.parse_args()

    if args.show_locations:
        print("IL file is located at:", il_file)
        print("WL file is located at:", wl_file)
        sys.exit(0)

    ignore_list = read_list_file(il_file) if args.il else None
    whitelist = read_list_file(wl_file) if args.wl else None
    
    # Whitelist mode: when --wl is used, ONLY collect whitelisted items
    whitelist_mode = args.wl

    save_project_structure_and_files('.', 'project_contents.txt', ignore_list, whitelist, whitelist_mode)

if __name__ == '__main__':
    main()
