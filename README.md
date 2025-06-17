# Terminal File Explorer App

A modern, terminal-based file explorer built with Textual, a Python TUI (Text User Interface) framework. This application allows you to browse your file system, view directory contents, and preview various file types directly from your terminal.

![Terminal File Explorer App](https://github.com/R0h1tAnand/windows-cli-explorer/blob/main/assets/demo.png)

## Features

- 📁 Browse file system directories and files in a familiar tree structure
- 📄 Preview text files with syntax highlighting for common file formats
- 🖼️ View basic information about images and open them in your system's default viewer
- 📄 Open PDF documents with your system's default PDF viewer
- 💻 Cross-platform support (Windows, macOS, Linux)
- 🔍 Easy navigation with keyboard controls
- ⚡ Fast and lightweight

## Supported File Types

### Text Files (with syntax highlighting)
- Python (.py)
- Markdown (.md)
- HTML (.html)
- CSS (.css)
- JavaScript (.js)
- JSON (.json)
- XML (.xml)
- CSV (.csv)
- YAML (.yaml, .yml)
- Plain text (.txt)

### Image Files
- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- GIF (.gif)

### Other Files
- PDF (.pdf) - Opens in system viewer

## Requirements

- Python 3.7+
- Textual library (`pip install textual`)
- Pillow library (`pip install pillow`)

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install textual pillow
```

## Usage

Run the file explorer app with:

```bash
python file_explorer_app.py
```

### Controls

- Use the **arrow keys** to navigate the file tree
- Press **Enter** to expand/collapse directories or select files
- Press **q** to quit the application

## How It Works

The application uses:
- Textual's `Tree` widget for the file system navigation
- Markdown widget to display file contents and information
- PIL (Python Imaging Library) to read basic image information
- System calls to open files in their default applications when necessary

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Textual](https://github.com/Textualize/textual) - The TUI framework powering this application
- [Pillow](https://python-pillow.org/) - For image processing capabilities

## Author

Rohit Anand

---

Feel free to contribute to this project by submitting issues or pull requests!
