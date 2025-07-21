import os
import tempfile
from src.plumbing.hash_object import hash_object

def write_tree(git_dir=".mygit", index_path=".mygit/index"):
    tree_entries = []
    with open(index_path) as idx:
        for line in idx:
            mode, path, sha1 = line.strip().split()
            tree_entries.append(f"{mode} {path} {sha1}")

    tree_content = "\n".join(tree_entries)
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(tree_content)
        tmp.flush()
        tree_sha1 = hash_object(tmp.name, git_dir, write=True)
    print(tree_sha1)

if __name__ == "__main__":
    write_tree()