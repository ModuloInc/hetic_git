import typer
import sys
import os

# Add the project path to sys.path to allow module imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.porcelain.init import init as init_func

app = typer.Typer(name="mygit", help="A Python implementation of Git")

@app.command()
def init(
    path: str = typer.Argument(".", help="Path where to initialize the repository")
):
    """
    Initialize a new MyGit repository at the specified path.
    """
    init_func(path)
    typer.echo(f"Git repository initialized in {path}")

if __name__ == "__main__":
    app()
