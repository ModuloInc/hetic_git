
import os
import sys
from src.plumbing.hash_object import hash_object

def add(file_path, git_dir=".mygit", index_path=".mygit/index"):
    """
    Add a file to the index (staging area).
    Args:
        file_path (str): Path to the file to add.
        git_dir (str): Path to the .mygit directory.
        index_path (str): Path to the index file.
    """
    import io

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    hash_object(file_path, git_dir, write=True)
    sha1 = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout

    mode = "100644"
    rel_path = os.path.relpath(file_path)
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "a") as idx:
        idx.write(f"{mode} {rel_path} {sha1}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add.py <file_path> [<git_dir>]", file=sys.stderr)
        sys.exit(1)
    file_path = sys.argv[1]
    git_dir = sys.argv[2] if len(sys.argv) > 2 else ".mygit"
    add(file_path, git_dir)