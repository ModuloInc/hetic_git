import os
import sys
import re

def rev_parse(ref, git_dir=".mygit"):
    """
    Resolve a reference (branch, tag, HEAD, or SHA-1) to its commit SHA-1.
    Args:
        ref (str): Reference name or SHA-1.
        git_dir (str): Path to the .mygit directory.
    Returns:
        str: The resolved SHA-1 string.
    """
    # 1. If it's a full SHA-1 (40 hex characters)
    if re.fullmatch(r"[0-9a-fA-F]{40}", ref):
        obj_path = os.path.join(git_dir, "objects", ref[:2], ref[2:])
        if os.path.exists(obj_path):
            print(ref)
            return ref
        else:
            print(f"Error: object {ref} does not exist.", file=sys.stderr)
            sys.exit(1)

    # 2. If it's HEAD
    if ref == "HEAD":
        head_path = os.path.join(git_dir, "HEAD")
        if not os.path.exists(head_path):
            print("Error: HEAD not found.", file=sys.stderr)
            sys.exit(1)
        with open(head_path) as f:
            content = f.read().strip()
        if content.startswith("ref: "):
            ref = content[5:].strip()
        else:
            # HEAD contains a SHA-1 directly
            if re.fullmatch(r"[0-9a-fA-F]{40}", content):
                print(content)
                return content
            else:
                print("Error: Invalid HEAD.", file=sys.stderr)
                sys.exit(1)

    # 3. If it's a reference (branch or tag)
    # Search in heads, then tags, then absolute ref
    for ref_path in [
        os.path.join(git_dir, "refs", "heads", ref),
        os.path.join(git_dir, "refs", "tags", ref),
        os.path.join(git_dir, ref) if ref.startswith("refs/") else None
    ]:
        if ref_path and os.path.exists(ref_path):
            with open(ref_path) as f:
                sha = f.read().strip()
            print(sha)
            return sha

    print(f"Error: reference '{ref}' not found.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rev_parse.py <ref> [<git_dir>]", file=sys.stderr)
        sys.exit(1)
    ref = sys.argv[1]
    git_dir = sys.argv[2] if len(sys.argv) > 2 else ".mygit"
    rev_parse(ref, git_dir) 