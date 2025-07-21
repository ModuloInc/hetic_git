import sys
import os
import hashlib
import zlib
from datetime import datetime

def commit_tree(tree_sha, message, parent=None, git_dir=".mygit"):
    # Construction du contenu du commit

    lines = [f"tree {tree_sha}"]
    if parent:
        lines.append(f"parent {parent}")
    author = f"Author <author@example.com> {int(datetime.now().timestamp())} +0000"
    committer = author
    lines.append(f"author {author}")
    lines.append(f"committer {committer}")
    lines.append("")
    lines.append(message)
    content = "\n".join(lines).encode()
    header = f"commit {len(content)}\0".encode()
    full_data = header + content
    sha1 = hashlib.sha1(full_data).hexdigest()
    # Écriture de l'objet

    obj_dir = os.path.join(git_dir, "objects", sha1[:2])
    obj_path = os.path.join(obj_dir, sha1[2:])
    os.makedirs(obj_dir, exist_ok=True)
    compressed = zlib.compress(full_data)
    with open(obj_path, 'wb') as f:
        f.write(compressed)
    print(sha1)
    return sha1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a commit object")
    parser.add_argument("tree_sha", help="SHA of the tree object")
    parser.add_argument("-m", "--message", required=True, help="Commit message")
    parser.add_argument("-p", "--parent", help="Parent commit SHA")
    parser.add_argument("--git-dir", default=".mygit", help="Git directory")
    args = parser.parse_args()
    commit_tree(args.tree_sha, args.message, args.parent, args.git_dir) 