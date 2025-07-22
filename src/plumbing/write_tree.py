import os
from src.plumbing.hash_object import hash_object_data

def write_tree(git_dir=".mygit", index_path=".mygit/index"):
    """
    Write the current index as a tree object and return its SHA-1.
    Args:
        git_dir (str): Path to the .mygit directory.
        index_path (str): Path to the index file.
    Returns:
        str: The SHA-1 of the created tree object.
    """
    tree_entries = []
    with open(index_path) as idx:
        for line in idx:
            mode, path, sha1 = line.strip().split()
            tree_entries.append(f"{mode} {path} {sha1}")

    tree_content = "\n".join(tree_entries)
    tree_sha1 = hash_object_data(tree_content, "tree", git_dir, write=True)
    return tree_sha1

if __name__ == "__main__":
    print(write_tree())
