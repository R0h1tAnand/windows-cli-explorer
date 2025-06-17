import os
import string
import mimetypes
import platform
import subprocess
from pathlib import Path
from PIL import Image

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Markdown, Tree
from textual.widgets.tree import TreeNode


def get_windows_drives() -> list[Path]:
    return [Path(f"{d}:\\") for d in string.ascii_uppercase if Path(f"{d}:\\").exists()]


TEXT_FILE_EXTENSIONS = {
    ".txt": "plaintext",
    ".md": "markdown",
    ".py": "python",
    ".json": "json",
    ".html": "html",
    ".css": "css",
    ".js": "javascript",
    ".xml": "xml",
    ".csv": "csv",
    ".yaml": "yaml",
    ".yml": "yaml",
}


def is_text_file(path: Path) -> bool:
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type is not None and mime_type.startswith("text")


def get_language_for_extension(ext: str) -> str:
    return TEXT_FILE_EXTENSIONS.get(ext.lower(), "")


class FileExplorerApp(App):
    """A terminal file explorer app with external image and PDF preview support."""

    BINDINGS = [("q", "quit", "Quit")]

    CSS = """
    Tree {
        width: 1fr;
        height: 1fr;
    }
    Markdown {
        width: 2fr;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree("My Computer", id="tree")
            yield Markdown("Select a file to view its contents", id="markdown")
        yield Footer()

    async def on_mount(self) -> None:
        tree = self.query_one("#tree", Tree)
        drives = get_windows_drives()

        if not drives:
            current_dir = Path(".")
            node = tree.root.add(
                f"Current Directory ({current_dir.absolute()})", current_dir.absolute()
            )
            await self.populate_node(node, current_dir.absolute())
        else:
            for drive in drives:
                node = tree.root.add(str(drive), drive)
                node.allow_expand = True  # Enable lazy expansion

        tree.root.expand()

    async def populate_node(self, node: TreeNode, path: Path) -> None:
        try:
            items = sorted(
                path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())
            )
            for item in items:
                if item.is_dir():
                    child = node.add(f"📁 {item.name}", item)
                    child.allow_expand = True
                elif item.is_file():
                    node.add(f"📄 {item.name}", item)
        except (PermissionError, OSError):
            node.add("Access denied", None)

    async def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node = event.node
        path = node.data
        if isinstance(path, Path) and path.is_dir() and not node.children:
            await self.populate_node(node, path)

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        path = event.node.data
        markdown_widget = self.query_one("#markdown", Markdown)

        if isinstance(path, Path):
            ext = path.suffix.lower()
            if path.is_file():
                if is_text_file(path) or ext in TEXT_FILE_EXTENSIONS:
                    try:
                        content = path.read_text(encoding="utf-8", errors="ignore")
                        language = get_language_for_extension(ext)
                        markdown_widget.update(
                            f"# {path.name}\n\n```{language}\n{content}\n```"
                        )
                    except Exception as e:
                        markdown_widget.update(
                            f"# {path.name}\n\n**Error reading file:** {e}"
                        )

                elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
                    try:
                        with Image.open(path) as img:
                            info = f"# {path.name}\n\n"
                            info += f"**Format:** {img.format}\n\n"
                            info += f"**Size:** {img.size[0]}x{img.size[1]} px\n\n"
                            info += f"**Mode:** {img.mode}\n\n"
                            info += "👉 Opening image in system viewer..."
                            markdown_widget.update(info)
                        self.open_in_system_viewer(path)
                    except Exception as e:
                        markdown_widget.update(
                            f"# {path.name}\n\n**Error reading image:** {e}"
                        )

                elif ext == ".pdf":
                    markdown_widget.update(
                        f"# {path.name}\n\n*PDF preview not supported in terminal.*\n\n👉 Opening PDF externally..."
                    )
                    self.open_in_system_viewer(path)

                else:
                    markdown_widget.update(
                        f"# {path.name}\n\n*Preview not available for this file type.*"
                    )

            elif path.is_dir():
                try:
                    items = list(path.iterdir())
                    content = f"# Directory: {path}\n\n"
                    content += f"**Total items:** {len(items)}\n\n"

                    dirs = [item for item in items if item.is_dir()]
                    files = [item for item in items if item.is_file()]

                    if dirs:
                        content += "## Directories:\n"
                        for d in dirs[:10]:
                            content += f"- 📁 {d.name}\n"
                        if len(dirs) > 10:
                            content += f"- ... and {len(dirs) - 10} more directories\n"

                    if files:
                        content += "\n## Files:\n"
                        for f in files[:10]:
                            content += f"- 📄 {f.name}\n"
                        if len(files) > 10:
                            content += f"- ... and {len(files) - 10} more files\n"

                    markdown_widget.update(content)
                except Exception as e:
                    markdown_widget.update(
                        f"# {path}\n\n**Error accessing directory:** {e}"
                    )
        else:
            markdown_widget.update("")

    def open_in_system_viewer(self, path: Path) -> None:
        """Open the file with the default system viewer."""
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", str(path)], check=False)
            else:
                subprocess.run(["xdg-open", str(path)], check=False)
        except Exception as e:
            print(f"Failed to open file externally: {e}")


if __name__ == "__main__":
    app = FileExplorerApp()
    app.run()
