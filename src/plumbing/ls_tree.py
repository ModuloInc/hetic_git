import sys
from src.plumbing.cat_file import read_object

def ls_tree(tree_sha, git_dir=".mygit"):
    obj_type, content = read_object(tree_sha, git_dir)
    if obj_type != "tree":
        print(f"Object {tree_sha} is not a tree", file=sys.stderr)
        sys.exit(1)
    lines = content.decode().splitlines()
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 3:
            mode, path, sha1 = parts
            print(f"{mode} {sha1} {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ls_tree.py <tree_sha> [<git_dir>]", file=sys.stderr)
        sys.exit(1)
    tree_sha = sys.argv[1]
    git_dir = sys.argv[2] if len(sys.argv) > 2 else ".mygit"
    ls_tree(tree_sha, git_dir) 