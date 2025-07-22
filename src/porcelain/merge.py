import os
import sys
from src.porcelain.rev_parse import rev_parse
from src.plumbing.cat_file import read_object

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")

CONFLICT_START = "<<<<<<< HEAD\n"
CONFLICT_MID =   "=======\n"
CONFLICT_END =   ">>>>>>> MERGE_HEAD\n"

def parse_tree(tree_sha, git_dir=GIT_DIR):
    """
    Parse a tree object and return a dictionary of file entries.
    Args:
        tree_sha (str): SHA-1 of the tree object.
        git_dir (str): Path to the .mygit directory.
    Returns:
        dict: {path: (mode, sha1)}
    """
    obj_type, content = read_object(tree_sha, git_dir)
    if obj_type != "tree":
        raise Exception(f"Object {tree_sha} is not a tree")
    entries = {}
    for line in content.decode().splitlines():
        mode, path, sha1 = line.strip().split()
        entries[path] = (mode, sha1)
    return entries

def find_merge_base(head_sha, target_sha, git_dir=GIT_DIR):
    """
    Find the common ancestor (merge base) of two commits.
    Args:
        head_sha (str): SHA-1 of HEAD commit.
        target_sha (str): SHA-1 of target commit.
        git_dir (str): Path to the .mygit directory.
    Returns:
        str or None: SHA-1 of the merge base, or None if not found.
    """
    def get_ancestors(sha):
        ancestors = set()
        stack = [sha]
        while stack:
            s = stack.pop()
            if s in ancestors:
                continue
            ancestors.add(s)
            obj_type, content = read_object(s, git_dir)
            if obj_type != "commit":
                continue
            for line in content.decode().splitlines():
                if line.startswith("parent "):
                    stack.append(line[7:].strip())
        return ancestors
    head_anc = get_ancestors(head_sha)
    target_anc = get_ancestors(target_sha)
    common = head_anc & target_anc
    if not common:
        return None
    # Return the closest common ancestor (not optimal, but works for simple cases)
    for s in [head_sha, target_sha]:
        if s in common:
            return s
    for s in head_anc:
        if s in common:
            return s
    return list(common)[0]

def merge_trees(base, head, target, git_dir=GIT_DIR):
    """
    Merge three trees and detect conflicts.
    Args:
        base (dict): Base tree entries.
        head (dict): HEAD tree entries.
        target (dict): Target tree entries.
        git_dir (str): Path to the .mygit directory.
    Returns:
        tuple: (merged dict, set of conflict paths)
    """
    merged = {}
    conflicts = set()
    all_files = set(base.keys()) | set(head.keys()) | set(target.keys())
    for path in all_files:
        base_entry = base.get(path)
        head_entry = head.get(path)
        target_entry = target.get(path)
        if head_entry == target_entry:
            merged[path] = head_entry
        elif base_entry == head_entry:
            merged[path] = target_entry
        elif base_entry == target_entry:
            merged[path] = head_entry
        else:
            # Conflict: both changed differently
            merged[path] = None
            conflicts.add(path)
    return merged, conflicts

def read_blob(sha, git_dir=GIT_DIR):
    """
    Read a blob object and return its content.
    Args:
        sha (str): SHA-1 of the blob object.
        git_dir (str): Path to the .mygit directory.
    Returns:
        bytes: Blob content.
    """
    obj_type, content = read_object(sha, git_dir)
    if obj_type != "blob":
        raise Exception(f"Object {sha} is not a blob")
    return content

def write_conflict_file(path, head_sha, target_sha, git_dir=GIT_DIR):
    """
    Write a file with conflict markers for a merge conflict.
    Args:
        path (str): Path to the conflicted file.
        head_sha (str): SHA-1 of the HEAD version.
        target_sha (str): SHA-1 of the target version.
        git_dir (str): Path to the .mygit directory.
    """
    head_content = read_blob(head_sha, git_dir).decode(errors="replace") if head_sha else ""
    target_content = read_blob(target_sha, git_dir).decode(errors="replace") if target_sha else ""
    with open(path, "w") as f:
        f.write(CONFLICT_START)
        f.write(head_content)
        f.write(CONFLICT_MID)
        f.write(target_content)
        f.write(CONFLICT_END)

def merge(target_ref, git_dir=GIT_DIR, index_path=INDEX_FILE):
    """
    Merge the target branch or commit into HEAD.
    Args:
        target_ref (str): Target branch or commit to merge.
        git_dir (str): Path to the .mygit directory.
        index_path (str): Path to the index file.
    Returns:
        bool: True if merge was successful, False if there were conflicts or errors.
    """
    head_sha = rev_parse("HEAD", git_dir)
    target_sha = rev_parse(target_ref, git_dir)
    if head_sha == target_sha:
        print("Already up to date.")
        return True
    # Find merge base
    base_sha = find_merge_base(head_sha, target_sha, git_dir)
    if not base_sha:
        print("No common ancestor found. Cannot merge.")
        return False
    # Read trees
    obj_type, head_commit = read_object(head_sha, git_dir)
    obj_type, target_commit = read_object(target_sha, git_dir)
    obj_type, base_commit = read_object(base_sha, git_dir)
    head_tree = parse_tree([l for l in head_commit.decode().splitlines() if l.startswith('tree ')][0][5:].strip(), git_dir)
    target_tree = parse_tree([l for l in target_commit.decode().splitlines() if l.startswith('tree ')][0][5:].strip(), git_dir)
    base_tree = parse_tree([l for l in base_commit.decode().splitlines() if l.startswith('tree ')][0][5:].strip(), git_dir)
    # Merge
    merged, conflicts = merge_trees(base_tree, head_tree, target_tree, git_dir)
    # Write merged files to working directory and index
    with open(index_path, "w") as idx:
        for path, entry in merged.items():
            if entry is None:
                # Conflict
                head_entry = head_tree.get(path)
                target_entry = target_tree.get(path)
                head_sha = head_entry[1] if head_entry else None
                target_sha = target_entry[1] if target_entry else None
                write_conflict_file(path, head_sha, target_sha, git_dir)
                idx.write(f"100644 {path} CONFLICT\n")
            else:
                mode, sha1 = entry
                obj_type, blob_content = read_object(sha1, git_dir)
                if obj_type == "blob":
                    dir_path = os.path.dirname(path)
                    if dir_path:
                        os.makedirs(dir_path, exist_ok=True)
                    with open(path, "wb") as f:
                        f.write(blob_content)
                    idx.write(f"{mode} {path} {sha1}\n")
    if conflicts:
        print(f"Merge completed with conflicts in: {', '.join(conflicts)}")
        print("Please resolve conflicts and commit.")
        return False
    # Write merged tree
    from src.plumbing.hash_object import hash_object_data
    from src.plumbing.commit_tree import commit_tree
    tree_entries = []
    for path, entry in merged.items():
        if entry is not None:
            mode, sha1 = entry
            tree_entries.append(f"{mode} {path} {sha1}")
    tree_content = "\n".join(tree_entries)
    tree_sha = hash_object_data(tree_content, "tree", git_dir, write=True)
    # Create merge commit with two parents
    message = f"Merge commit {target_ref} into HEAD"
    # Use plumbing commit_tree for two parents
    sha1 = commit_tree(tree_sha, message, [head_sha, target_sha], git_dir)
    print(f"Merge commit created: {sha1}")
    # Update HEAD
    head_path = os.path.join(git_dir, "HEAD")
    with open(head_path) as f:
        content = f.read().strip()
    if content.startswith("ref: "):
        ref_rel = content[5:].strip()
        ref_path = os.path.join(git_dir, ref_rel)
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        with open(ref_path, "w") as rf:
            rf.write(sha1 + "\n")
    else:
        with open(head_path, "w") as f:
            f.write(sha1 + "\n")
    print("Merge successful.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python merge.py <branch|sha>", file=sys.stderr)
        sys.exit(1)
    merge(sys.argv[1])
