import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

def init(directory="."):
    """
    Initialize a new MyGit repository in the specified directory.
    Creates the .mygit directory structure and default config files.
    Args:
        directory (str): Target directory for repository initialization. Defaults to current directory.
    Returns:
        bool: True if initialization succeeded, False otherwise.
    """
    git_dir = os.path.join(directory, ".mygit")
    console = Console()

    if os.path.exists(git_dir):
        console.print(f"Git repository is already initialized in {os.path.abspath(directory)}", style="bold red")
        return False

    try:
        dirs = [
            git_dir,
            os.path.join(git_dir, "objects"),
            os.path.join(git_dir, "refs"),
            os.path.join(git_dir, "refs/heads"),
            os.path.join(git_dir, "refs/tags"),
        ]

        for d in dirs:
            os.makedirs(d)

        with open(os.path.join(git_dir, "HEAD"), "w") as f:
            f.write("ref: refs/heads/main\n")

        with open(os.path.join(git_dir, "config"), "w") as f:
            f.write("[core]\n")
            f.write("\trepositoryformatversion = 0\n")
            f.write("\tfilemode = true\n")
            f.write("\tbare = false\n")

        ascii_art = """
    _._     _,-'""`-._         H   H  EEEEE  L      L       OOO  
   (,-.`._,'(       |\`-/|     H   H  E      L      L      O   O 
       `-.-' \ )-`( , o o)     HHHHH  EEEEE  L      L      O   O 
             `-    \`_`"'-     H   H  E      L      L      O   O 
                               H   H  EEEEE  LLLLL  LLLLL   OOO  
"""
        console.print(Panel(Text(ascii_art, style="bold cyan"), title="[bold green]Welcome to MyGit[/bold green]", border_style="green"))

        console.print(f"Git repository initialized in [bold green]{os.path.abspath(directory)}[/bold green]\n")

        table = Table(title="MyGit Basic Commands", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="dim", width=20)
        table.add_column("Description")

        table.add_row("git add <file>", "Add a file to the staging area")
        table.add_row("git commit -m <message>", "Record changes to a new commit")
        table.add_row("git status", "Show the state of your working directory")
        table.add_row("git log", "Show commit history")

        console.print(table)

        return True

    except Exception as e:
        console.print(f"Error initializing Git repository: {e}", style="bold red")
        return False

if __name__ == "__main__":
    target_dir = "."
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]

    init(target_dir)
