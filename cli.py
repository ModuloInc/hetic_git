import typer
import sys
import os

# Ajout du chemin du projet au sys.path pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.porcelain.init import init as init_func

app = typer.Typer(name="mygit", help="Une implémentation de Git en Python")

@app.command()
def init(
    path: str = typer.Argument(".", help="Chemin où initialiser le dépôt")
):
    init_func(path)
    typer.echo(f"Dépôt Git initialisé dans {path}")

if __name__ == "__main__":
    app()
