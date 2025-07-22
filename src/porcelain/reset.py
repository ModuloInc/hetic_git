import os
import sys
from src.porcelain.rev_parse import rev_parse
from src.plumbing.cat_file import read_object

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")


def parse_commit(content):
    """
    Parse the content of a commit object and extract its information.
    Args:
        content (bytes): The raw content of the commit object.
    Returns:
        dict: Parsed commit information (tree, parent, author, committer).
    """
    lines = content.decode().splitlines()
    commit_info = {}
    for line in lines:
        if line.startswith('tree '):
            commit_info['tree'] = line[5:].strip()
        elif line.startswith('parent '):
            commit_info['parent'] = line[7:].strip()
        elif line.startswith('author '):
            commit_info['author'] = line[7:].strip()
        elif line.startswith('committer '):
            commit_info['committer'] = line[10:].strip()
        elif line.strip() == '':
            break
    return commit_info

def reset(commit_ref, mode="mixed", git_dir=GIT_DIR, index_path=INDEX_FILE):
    """
    Reset HEAD, index, and working directory to a given commit.
    Args:
        commit_ref (str): Commit reference (SHA, HEAD, branch, etc.).
        mode (str): Reset mode: 'soft', 'mixed', or 'hard'.
        git_dir (str): Path to the .mygit directory.
        index_path (str): Path to the index file.
    """
    # 1. Resolve the commit
    commit_sha = rev_parse(commit_ref, git_dir)
    if not isinstance(commit_sha, str):
        # rev_parse may print and return None
        print(f"Unable to resolve {commit_ref}", file=sys.stderr)
        sys.exit(1)
    # 2. Read the commit object
    obj_type, commit_content = read_object(commit_sha, git_dir)
    if obj_type != "commit":
        print(f"{commit_sha} is not a commit.", file=sys.stderr)
        sys.exit(1)
    commit_info = parse_commit(commit_content)
    tree_sha = commit_info["tree"]
    # 3. --soft: move HEAD
    # HEAD can point to a ref or contain the SHA directly
    head_path = os.path.join(git_dir, "HEAD")
    with open(head_path) as f:
        head_content = f.read().strip()
    if head_content.startswith("ref: "):
        ref_rel = head_content[5:].strip()
        ref_path = os.path.join(git_dir, ref_rel)
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        with open(ref_path, "w") as rf:
            rf.write(commit_sha + "\n")
    else:
        with open(head_path, "w") as f:
            f.write(commit_sha + "\n")
    if mode == "soft":
        print(f"HEAD moved to {commit_sha}")
        return
    # 4. --mixed: reset the index
    obj_type, tree_content = read_object(tree_sha, git_dir)
    if obj_type != "tree":
        print(f"{tree_sha} is not a tree.", file=sys.stderr)
        sys.exit(1)
    # Overwrite the index with the tree content
    with open(index_path, "w") as idx:
        for line in tree_content.decode().splitlines():
            parts = line.strip().split()
            if len(parts) == 3:
                mode, path, sha1 = parts
                idx.write(f"{mode} {path} {sha1}\n")
    if mode == "mixed":
        print(f"Index reset to {tree_sha}")
        return
    # 5. --hard: reset the working directory
    for line in tree_content.decode().splitlines():
        parts = line.strip().split()
        if len(parts) == 3:
            mode, path, sha1 = parts
            obj_type, blob_content = read_object(sha1, git_dir)
            if obj_type != "blob":
                continue
            dir_path = os.path.dirname(path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(path, "wb") as f:
                f.write(blob_content)
    print(f"Working directory reset to {tree_sha}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reset HEAD, index, and working directory to a given commit.")
    parser.add_argument("commit_ref", help="Commit reference (SHA, HEAD, branch, etc.)")
    parser.add_argument("--soft", action="store_true", help="Move HEAD only")
    parser.add_argument("--mixed", action="store_true", help="Move HEAD and reset the index (default)")
    parser.add_argument("--hard", action="store_true", help="Move HEAD, reset the index and the working directory")
    parser.add_argument("--git-dir", default=GIT_DIR, help="Path to the .mygit directory")
    args = parser.parse_args()
    if args.soft:
        mode = "soft"
    elif args.hard:
        mode = "hard"
    else:
        mode = "mixed"
    reset(args.commit_ref, mode=mode, git_dir=args.git_dir, index_path=os.path.join(args.git_dir, "index")) 