# Snap2Txt

Snap2Txt is a Python utility that captures the structure and contents of a project directory and saves them into a text file. It's designed for quick documentation of your project's file system.

## Features

- **Complete Capture**: Records the entire file structure and contents of the project.
- **Customizable Filters**: Offers ignore and whitelist options for targeted scanning.
- **Command-Line Interface**: Simple and easy-to-use command-line tool.

## Installation

Install Snap2Txt with pip:

```bash
pip install snap2txt
```

> **Note**: The installation now automatically provides `.il` and `.wl` files along with the package.

## Usage

Navigate to your project directory and run:

```bash
snap2txt
```

By default, Snap2Txt will scan all files and directories in the current folder and produce an output file called `project_contents.txt`.

### Locate the .il and .wl Files

If you need to see where Snap2Txt’s `.il` and `.wl` files were installed on your system (e.g., to customize them), run:

```bash
snap2txt --show-locations
```

This will print the full path to each file, so you can open or edit them as needed.

### Optional Flags

- `--il`: Use ignore list defined in `.il`.
- `--wl`: Use whitelist defined in `.wl`.

Example:

```bash
snap2txt --il
```

```bash
snap2txt --wl
```

## Configuration

Snap2Txt respects two files for filtering:

1. **Ignore List (`.il`)**: Exclude certain files/directories.
2. **Whitelist (`.wl`)**: Include only certain files/directories.

By default, Snap2Txt installs a basic `.il` and `.wl` in the package directory. To tailor the behavior for your project, you can edit those files or replace them with your own custom rules.

> **Tip**: To quickly locate where these files were installed, use `snap2txt --show-locations`.

### Example `.il` File

```text
node_modules/
*.log
```

### Example `.wl` File

```text
*.py
*.md
```

## Contributing

Contributions to Snap2Txt are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## License

Snap2Txt is open-sourced software licensed under the [MIT license](LICENSE).

## Support

For support, questions, or feedback, please [open an issue](https://github.com/yourusername/snap2txt/issues) in the GitHub repository.