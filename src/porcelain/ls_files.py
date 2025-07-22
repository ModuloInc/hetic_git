import sys

def ls_files(index_path=".mygit/index"):
    """
    List all files currently tracked in the index (staging area).
    Args:
        index_path (str): Path to the index file.
    """
    try:
        with open(index_path) as idx:
            for line in idx:
                parts = line.strip().split()
                if len(parts) >= 2:
                    print(parts[1])
    except FileNotFoundError:
        print(f"Index file not found: {index_path}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    ls_files() 