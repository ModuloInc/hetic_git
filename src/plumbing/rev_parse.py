import os
import sys
import re

def rev_parse(ref, git_dir=".mygit"):
    # 1. Si c'est un SHA-1 complet (40 caractères hexadécimaux)
    if re.fullmatch(r"[0-9a-fA-F]{40}", ref):
        obj_path = os.path.join(git_dir, "objects", ref[:2], ref[2:])
        if os.path.exists(obj_path):
            print(ref)
            return ref
        else:
            print(f"Erreur : l'objet {ref} n'existe pas.", file=sys.stderr)
            sys.exit(1)

    # 2. Si c'est HEAD
    if ref == "HEAD":
        head_path = os.path.join(git_dir, "HEAD")
        if not os.path.exists(head_path):
            print("Erreur : HEAD introuvable.", file=sys.stderr)
            sys.exit(1)
        with open(head_path) as f:
            content = f.read().strip()
        if content.startswith("ref: "):
            ref = content[5:].strip()
        else:
            # HEAD contient directement un SHA-1
            if re.fullmatch(r"[0-9a-fA-F]{40}", content):
                print(content)
                return content
            else:
                print("Erreur : HEAD invalide.", file=sys.stderr)
                sys.exit(1)

    # 3. Si c'est une référence (branche ou tag)
    # Cherche d'abord dans heads, puis tags, puis ref absolu
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

    print(f"Erreur : référence '{ref}' introuvable.", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python rev_parse.py <ref> [<git_dir>]", file=sys.stderr)
        sys.exit(1)
    ref = sys.argv[1]
    git_dir = sys.argv[2] if len(sys.argv) > 2 else ".mygit"
    rev_parse(ref, git_dir) 