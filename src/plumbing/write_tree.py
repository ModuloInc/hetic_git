import os
from src.plumbing.hash_object import hash_object_data

def write_tree(git_dir=".mygit", index_path=".mygit/index"):
    entries = []
    with open(index_path) as idx:
        for line in idx:
            mode, path, sha1 = line.strip().split()
            # Format attendu : <mode> <nom>\0<sha1 binaire>
            entry = f"{mode} {path}".encode() + b"\0" + bytes.fromhex(sha1)
            entries.append(entry)
    tree_content = b"".join(entries)
    tree_sha1 = hash_object_data(tree_content, "tree", git_dir, write=True)
    print(tree_sha1)

if __name__ == "__main__":
    write_tree()
