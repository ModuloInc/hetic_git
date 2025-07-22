import typer
import sys
import os

# Add the project path to sys.path to allow module imports
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
from src.porcelain.status import status as status_func
app = typer.Typer(name="mygit", help="A Python implementation of Git")

plumbing_app = typer.Typer(help="Plumbing (low-level) commands")
app.add_typer(plumbing_app, name="plumbing")

@app.command()
def init(
    path: str = typer.Argument(".", help="Path where to initialize the repository")
):
    """
    Initialize a new MyGit repository at the specified path.
    """
    init_func(path)
    typer.echo(f"Git repository initialized in {path}")

@app.command("hash-object")
@plumbing_app.command("hash-object")
def hash_object(
    file: str = typer.Argument(..., help="File to hash"),
    write: bool = typer.Option(False, "--write", "-w", help="Write the object to the Git database")
):
    """
    Compute the hash of a file and optionally write it to the Git database.
    """
    hash_object_func(file, write=write)
    if write:
        typer.echo(f"Hash for file {file} computed and written to the database")
    else:
        typer.echo(f"Hash for file {file} computed")

@app.command("add")
@plumbing_app.command("add")
def add(
    file: str = typer.Argument(..., help="File to add to the index")
):
    """
    Add a file to the index (staging area).
    """
    add_func(file)
    typer.echo(f"File {file} added to the index")

@app.command("cat-file")
@plumbing_app.command("cat-file")
def cat_file(
    oid: str = typer.Argument(..., help="OID of the object to read"),
    type_: bool = typer.Option(False, "--type", "-t", help="Show the type of the object"),
    pretty: bool = typer.Option(False, "--pretty", "-p", help="Show the formatted content of the object"),
    git_dir: str = typer.Option(".mygit", help="Path to the .mygit directory")
):
    """
    Show the type or content of a Git object (blob/tree/commit).
    """
    if type_ == pretty:
        typer.echo("You must specify either --type/-t or --pretty/-p, but not both.", err=True)
        raise typer.Exit(1)
    opt = "-t" if type_ else "-p"
    cat_file_func(oid, opt, git_dir)

@app.command("write-tree")
def write_tree():
    """
    Write the current index as a tree object and print its SHA-1.
    """
    write_tree_func()
    typer.echo("Tree written")

@app.command("commit-tree")
@plumbing_app.command("commit-tree")
def commit_tree_cmd(
    tree_sha: str = typer.Argument(..., help="SHA of the tree object"),
    message: str = typer.Option(..., "-m", "--message", help="Commit message"),
    parent: str = typer.Option(None, "-p", "--parent", help="Parent commit SHA"),
    git_dir: str = typer.Option(".mygit", help="Path to the .mygit directory")
):
    """
    Create a commit object from a tree and print its OID.
    """
    commit_tree_func(tree_sha, message, parent, git_dir)

@app.command("commit")
def commit_cmd(
    message: str = typer.Option(..., "-m", "--message", help="Commit message")
):
    """
    Create a new commit from the current index.
    """
    commit_func(message)
    typer.echo("Commit created")
    
@app.command("ls-tree")
def ls_tree_cmd(tree_sha: str, git_dir: str = ".mygit"):
    """
    List the contents of a tree object (like git ls-tree).
    """
    ls_tree_func(tree_sha, git_dir)
    
@app.command("ls-files")
def ls_files_cmd():
    """
    List all files in the index (like git ls-files).
    """
    ls_files_func()

@app.command("show-ref")
@plumbing_app.command("show-ref")
def show_ref_cmd(git_dir: str = ".mygit"):
    """
    List all refs and their hashes (branches and tags).
    """
    show_ref_func(git_dir)

@app.command("rev-parse")
@plumbing_app.command("rev-parse")
def rev_parse_cmd(
    ref: str = typer.Argument(..., help="Reference to resolve (branch, HEAD, SHA-1, tag)"),
    git_dir: str = typer.Option(".mygit", help="Path to the .mygit directory")
):
    """
    Resolve a reference (branch, HEAD, tag, SHA-1) to a SHA-1.
    """
    rev_parse_func(ref, git_dir)

@app.command("log")
def log_cmd():
    """
    Show the commit history from HEAD (like git log).
    """
    log_func()

@app.command("rm")
def rm_cmd(
    file: str = typer.Argument(..., help="File to remove from the index and working directory"),
    cached: bool = typer.Option(False, "--cached", help="Only remove from index, not from working directory")
):
    """
    Remove a file from the index and optionally from the working directory.
    """
    if not cached:
        if not typer.confirm(f"Are you sure you want to remove {file} from the working directory?"):
            typer.echo("Removal cancelled.")
            raise typer.Exit(0)
    rm_func(file, cached=cached)
    if cached:
        typer.echo(f"File {file} removed from index only.")
    else:
        typer.echo(f"File {file} removed from index and working directory.")

@app.command("reset")
def reset_cmd(
    commit_ref: str = typer.Argument(..., help="Commit reference (SHA, HEAD, branch, etc.)"),
    soft: bool = typer.Option(False, "--soft", help="Move HEAD only"),
    mixed: bool = typer.Option(False, "--mixed", help="Move HEAD and reset the index (default)"),
    hard: bool = typer.Option(False, "--hard", help="Move HEAD, reset the index and the working directory")
):
    """
    Reset HEAD, index, and working directory to a given commit.
    """
    if soft:
        mode = "soft"
    elif hard:
        mode = "hard"
    else:
        mode = "mixed"
    reset_func(commit_ref, mode=mode)
    typer.echo(f"reset --{mode} performed on {commit_ref}")

@app.command("checkout")
def checkout_cmd(
    target: str = typer.Argument(None, help="Branch name or SHA to checkout"),
    b: str = typer.Option(None, "-b", help="Create a new branch and check it out"),
    ctx: typer.Context = typer.Option(None, hidden=True)
):
    """
    Switch to a branch or commit. Use -b <branch> to create a branch.
    """
    if not target and not b:
        typer.echo("Error: Missing argument 'TARGET' or option '-b'.", err=True)
        raise typer.Exit(1)
        
    actual_target = b if b else target
    
    git_dir = ctx.obj.git_dir if ctx and hasattr(ctx.obj, 'git_dir') else ".mygit"
    checkout_func(actual_target, create_branch=b, git_dir=git_dir)
    typer.echo(f"Checkout performed on {b if b else target}")

@app.command("status")
def status_cmd(ctx: typer.Context = typer.Option(None, hidden=True)):
    status_func()

@app.command("merge")
def merge_cmd(
    target: str = typer.Argument(..., help="Branch name or SHA to merge into HEAD")
):
    """
    Merge the target branch or commit into HEAD (3-way merge, merge commit, conflict management).
    """
    success = merge_func(target)
    if success:
        typer.echo(f"Merge of {target} completed successfully.")

def main():
    app()

if __name__ == "__main__":
    app()