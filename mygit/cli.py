import typer
import sys
import os
from typing import Optional

# Ajout du chemin du projet au sys.path pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.porcelain.init import init as init_func
from src.plumbing.hash_object import hash_object as hash_object_func
from src.porcelain.add import add as add_func

app = typer.Typer(name="mygit", help="Une implémentation de Git en Python")

plumbing_app = typer.Typer(help="Commandes plumbing (bas niveau)")
app.add_typer(plumbing_app, name="plumbing")

@app.command()
def init(
    path: str = typer.Argument(".", help="Chemin où initialiser le dépôt")
):
    init_func(path)
    typer.echo(f"Dépôt Git initialisé dans {path}")

@app.command("hash-object")
@plumbing_app.command("hash-object")
def hash_object(
    file: str = typer.Argument(..., help="Fichier à hasher"),
    write: bool = typer.Option(False, "--write", "-w", help="Écrire l'objet dans la base de données Git")
):

    hash_object_func(file, write=write)
    if write:
        typer.echo(f"Hash du fichier {file} calculé et écrit dans la base de données")
    else:
        typer.echo(f"Hash du fichier {file} calculé")

@app.command()
def add(
    file: str = typer.Argument(..., help="Fichier à ajouter à l'index")
):
    add_func(file)
    typer.echo(f"Fichier {file} ajouté à l'index")

if __name__ == "__main__":
    app()
