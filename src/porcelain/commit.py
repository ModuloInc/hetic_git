# python
import os
import time
import hashlib
import zlib

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")
COMMITS_DIR = os.path.join(GIT_DIR, "commits")

# python
def read_index():
    index = {}
    if not os.path.exists(INDEX_FILE):
        return index
    with open(INDEX_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(" ")
            if len(parts) == 3:
                _, filename, sha1 = parts
                index[filename] = sha1
    return index

from src.plumbing.write_tree import write_tree

def commit(message):
    os.makedirs(COMMITS_DIR, exist_ok=True)
    index = read_index()
    timestamp = int(time.time())
    # 1. Générer le tree à partir de l'index
    tree_sha = write_tree()
    # 2. Construire le contenu du commit avec la ligne tree
    content_str = f"tree {tree_sha}\n"
    content_str += f"message: {message}\ntimestamp: {timestamp}\n"
    for fname, sha1 in index.items():
        content_str += f"  {fname}: {sha1}\n"
    # Format Git: header + contenu
    header = f"commit {len(content_str)}\0".encode()
    full_data = header + content_str.encode()
    commit_hash = hashlib.sha1(full_data).hexdigest()
    # Stocker l'objet commit dans .mygit/objects/
    obj_dir = os.path.join(GIT_DIR, "objects", commit_hash[:2])
    obj_path = os.path.join(obj_dir, commit_hash[2:])
    os.makedirs(obj_dir, exist_ok=True)
    compressed = zlib.compress(full_data)
    with open(obj_path, "wb") as f:
        f.write(compressed)
    # (Optionnel) écrire aussi dans .mygit/commits/ pour debug
    # commit_file = os.path.join(COMMITS_DIR, commit_hash)
    # with open(commit_file, "w") as f:
    #     f.write(content_str)
    print(f"Commit créé: {commit_hash}")

    head_path = os.path.join(GIT_DIR, "HEAD")
    if os.path.exists(head_path):
        with open(head_path) as f:
            content = f.read().strip()
        if content.startswith("ref: "):
            ref_rel = content[5:].strip()
            ref_path = os.path.join(GIT_DIR, ref_rel)
            os.makedirs(os.path.dirname(ref_path), exist_ok=True)
            with open(ref_path, "w") as rf:
                rf.write(commit_hash + "\n")

# Pour l’intégrer à ta CLI :
# from src.porcelain.commit import commit as commit_func
# @app.command("commit")
# def commit_cmd(message: str = typer.Argument(..., help="Message du commit")):
#     commit_func(message)