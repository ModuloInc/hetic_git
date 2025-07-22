import typer
import sys
import os

# Ajout du chemin du projet au sys.path pour pouvoir importer les modules
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.porcelain.init import init as init_func
from src.plumbing.hash_object import hash_object as hash_object_func
from src.plumbing.cat_file import cat_file as cat_file_func
from src.porcelain.add import add as add_func
from src.plumbing.commit_tree import commit_tree as commit_tree_func
from src.porcelain.commit import commit as commit_func
from src.porcelain.ls_tree import ls_tree as ls_tree_func
from src.plumbing.write_tree import write_tree as write_tree_func
from src.porcelain.ls_files import ls_files as ls_files_func
from src.porcelain.show_ref import show_ref as show_ref_func
from src.porcelain.rev_parse import rev_parse as rev_parse_func
from src.porcelain.log import log as log_func
from src.porcelain.rm import rm as rm_func
from src.porcelain.reset import reset as reset_func
from src.porcelain.checkout import checkout as checkout_func
from src.porcelain.merge import merge as merge_func

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

@app.command("add")
@plumbing_app.command("add")
def add(
    file: str = typer.Argument(..., help="Fichier à ajouter à l'index")
):
    add_func(file)
    typer.echo(f"Fichier {file} ajouté à l'index")

@app.command("cat-file")
@plumbing_app.command("cat-file")
def cat_file(
    oid: str = typer.Argument(..., help="OID de l'objet à lire"),
    type_: bool = typer.Option(False, "--type", "-t", help="Afficher le type de l'objet"),
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Afficher le contenu formaté de l'objet"),
    git_dir: str = typer.Option(".mygit", help="Chemin du dossier .mygit")
):
    """Affiche le type ou le contenu d'un objet Git (blob/tree/commit)"""
    if type_ == pretty:
        typer.echo("Vous devez spécifier soit --type/-t soit --pretty/-p, mais pas les deux.", err=True)
        raise typer.Exit(1)
    opt = "-t" if type_ else "-p"
    cat_file_func(oid, opt, git_dir)

@app.command("write-tree")
def write_tree():
    write_tree_func()
    typer.echo("Tree")

@app.command("commit-tree")
@plumbing_app.command("commit-tree")
def commit_tree_cmd(
    tree_sha: str = typer.Argument(..., help="SHA de l'objet tree"),
    message: str = typer.Option(..., "-m", "--message", help="Message du commit"),
    parent: str = typer.Option(None, "-p", "--parent", help="SHA du commit parent"),
    git_dir: str = typer.Option(".mygit", help="Chemin du dossier .mygit")
):
    """Crée un objet commit à partir d'un tree et écrit son oid sur stdout."""
    commit_tree_func(tree_sha, message, parent, git_dir)

@app.command("commit")
def commit_cmd(
    message: str = typer.Option(..., "-m", "--message", help="Message du commit")
):
    commit_func(message)
    typer.echo("Commit créé")
    
@app.command("ls-tree")
def ls_tree_cmd(tree_sha: str, git_dir: str = ".mygit"):
    """Liste le contenu d'un objet tree (comme git ls-tree)"""
    ls_tree_func(tree_sha, git_dir)
    
@app.command("ls-files")
def ls_files_cmd():
    """Liste tous les fichiers dans l'index (comme git ls-files)"""
    ls_files_func()

@app.command("show-ref")
@plumbing_app.command("show-ref")
def show_ref_cmd(git_dir: str = ".mygit"):
    """Liste toutes les refs et leurs hashes (branches et tags)"""
    show_ref_func(git_dir)

@app.command("rev-parse")
@plumbing_app.command("rev-parse")
def rev_parse_cmd(
    ref: str = typer.Argument(..., help="Référence à résoudre (branche, HEAD, SHA-1, tag)"),
    git_dir: str = typer.Option(".mygit", help="Chemin du dossier .mygit")
):
    """Résout une référence (branche, HEAD, tag, SHA-1) en SHA-1."""
    rev_parse_func(ref, git_dir)

@app.command("log")
def log_cmd():
    """Affiche l'historique des commits depuis HEAD (comme git log)"""
    log_func()

@app.command("rm")
def rm_cmd(
    file: str = typer.Argument(..., help="Fichier à supprimer de l'index et du répertoire de travail"),
    cached: bool = typer.Option(False, "--cached", help="Ne supprimer que de l'index, pas du répertoire de travail")
):
    if not cached:
        if not typer.confirm(f"Êtes-vous sûr de vouloir supprimer {file} du répertoire de travail ?"):
            typer.echo("Suppression annulée.")
            raise typer.Exit(0)
    rm_func(file, cached=cached)
    if cached:
        typer.echo(f"Fichier {file} supprimé de l'index seulement.")
    else:
        typer.echo(f"Fichier {file} supprimé de l'index et du répertoire de travail.")

@app.command("reset")
def reset_cmd(
    commit_ref: str = typer.Argument(..., help="Référence du commit (SHA, HEAD, branche, etc.)"),
    soft: bool = typer.Option(False, "--soft", help="Déplacer HEAD seulement"),
    mixed: bool = typer.Option(False, "--mixed", help="Déplacer HEAD et réinitialiser l'index (défaut)"),
    hard: bool = typer.Option(False, "--hard", help="Déplacer HEAD, réinitialiser l'index et le working directory")
):
    if soft:
        mode = "soft"
    elif hard:
        mode = "hard"
    else:
        mode = "mixed"
    reset_func(commit_ref, mode=mode)
    typer.echo(f"reset --{mode} effectué sur {commit_ref}")

@app.command("checkout")
def checkout_cmd(
    target: str = typer.Argument(..., help="Branche ou SHA à checkout"),
    b: str = typer.Option(None, "-b", help="Créer une nouvelle branche et la checkout")
):
    """Bascule sur une branche ou un commit. Utilisez -b <branche> pour créer une branche."""
    checkout_func(target, create_branch=b)
    typer.echo(f"Checkout effectué sur {b if b else target}")

@app.command("merge")
def merge_cmd(
    target: str = typer.Argument(..., help="Branche ou SHA à fusionner dans HEAD")
):
    """Fusionne la branche ou le commit cible dans HEAD (3-way merge, commit de merge, gestion des conflits)."""
    success = merge_func(target)
    if success:
        typer.echo(f"Merge de {target} terminé avec succès.")

if __name__ == "__main__":
    app()