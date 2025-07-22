import os
import sys

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")

def rm(file_path, git_dir=GIT_DIR, index_path=INDEX_FILE, cached=False):
    """
    Remove a file from the index and optionally from the working directory.
    Args:
        file_path (str): Path to the file to remove.
        git_dir (str): Path to the .mygit directory.
        index_path (str): Path to the index file.
        cached (bool): If True, only remove from index, not from working directory.
    """
    rel_path = os.path.relpath(file_path)
    # Remove from index
    if not os.path.exists(index_path):
        print(f"Index file not found: {index_path}", file=sys.stderr)
        sys.exit(1)
    new_lines = []
    removed = False
    with open(index_path, "r") as idx:
        for line in idx:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == rel_path:
                removed = True
                continue  # skip this line (removes from index)
            new_lines.append(line)
    if not removed:
        print(f"File '{rel_path}' not found in index.", file=sys.stderr)
        sys.exit(1)
    with open(index_path, "w") as idx:
        idx.writelines(new_lines)
    # Remove from working directory if not cached
    if not cached:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File '{file_path}' does not exist in working directory.", file=sys.stderr)
    print(f"Removed '{rel_path}'{' from index only' if cached else ''}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Remove file from working directory and index (like git rm)")
    parser.add_argument("file_path", help="Path to the file to remove")
    parser.add_argument("--cached", action="store_true", help="Only remove from index, not from working directory")
    parser.add_argument("--git-dir", default=GIT_DIR, help="Path to .mygit directory")
    args = parser.parse_args()
    rm(args.file_path, git_dir=args.git_dir, index_path=os.path.join(args.git_dir, "index"), cached=args.cached) 