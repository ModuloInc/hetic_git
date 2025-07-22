# python
import os
import time
import hashlib
import zlib
import io
import sys

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")
COMMITS_DIR = os.path.join(GIT_DIR, "commits")

def read_index():
    """
    Read the index file and return a dictionary mapping filenames to their SHA-1 hashes.
    Returns:
        dict: {filename: sha1}
    """
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
from src.porcelain.rev_parse import rev_parse

def commit(message):
    """
    Create a new commit from the current index and update HEAD.
    Args:
        message (str): Commit message.
    """
    os.makedirs(COMMITS_DIR, exist_ok=True)
    index = read_index()
    if not index:
        print("Nothing to commit, the index is empty.")
        return

    tree_sha = write_tree()
    content_str = f"tree {tree_sha}\n"
    
    parent_sha = None
    head_path = os.path.join(GIT_DIR, "HEAD")
    if os.path.exists(head_path):
        with open(head_path) as f:
            head_content = f.read().strip()
        if head_content:
            # We redirect stdout to avoid printing the SHA from rev_parse
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                parent_sha = rev_parse("HEAD", git_dir=GIT_DIR)
            except SystemExit: # rev_parse can exit on failure
                parent_sha = None
            finally:
                sys.stdout = old_stdout

    if parent_sha:
        content_str += f"parent {parent_sha}\n"
    
    timestamp = int(time.time())
    # 2. Build the commit content with the tree line
    content_str += f"message: {message}\ntimestamp: {timestamp}\n"
    for fname, sha1 in index.items():
        content_str += f"  {fname}: {sha1}\n"
    # Git format: header + content
    header = f"commit {len(content_str)}\0".encode()
    full_data = header + content_str.encode()
    commit_hash = hashlib.sha1(full_data).hexdigest()
    # Store the commit object in .mygit/objects/
    obj_dir = os.path.join(GIT_DIR, "objects", commit_hash[:2])
    obj_path = os.path.join(obj_dir, commit_hash[2:])
    os.makedirs(obj_dir, exist_ok=True)
    compressed = zlib.compress(full_data)
    with open(obj_path, "wb") as f:
        f.write(compressed)
    # (Optional) also write to .mygit/commits/ for debugging
    # commit_file = os.path.join(COMMITS_DIR, commit_hash)
    # with open(commit_file, "w") as f:
    #     f.write(content_str)
    print(f"Commit created: {commit_hash}")

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

# For CLI integration:
# from src.porcelain.commit import commit as commit_func
# @app.command("commit")
# def commit_cmd(message: str = typer.Argument(..., help="Commit message")):
#     commit_func(message)