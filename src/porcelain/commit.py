# python
import os
import time

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


def commit(message):
    os.makedirs(COMMITS_DIR, exist_ok=True)
    index = read_index()
    timestamp = int(time.time())
    commit_hash = str(timestamp)  # Simple hash, à améliorer plus tard
    commit_file = os.path.join(COMMITS_DIR, commit_hash)
    with open(commit_file, "w") as f:
        f.write(f"message: {message}\n")
        f.write(f"timestamp: {timestamp}\n")
        f.write("files:\n")
        for fname, sha1 in index.items():
            f.write(f"  {fname}: {sha1}\n")
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