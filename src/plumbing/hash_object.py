import sys
import os
import hashlib
import zlib


def hash_object(file_path, git_dir=".git", write=True):
    if not os.path.isfile(file_path):
        print(f"Erreur : '{file_path}' est introuvable ou n'est pas un fichier.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'rb') as f:
        data = f.read()

    header = f"blob {len(data)}\0".encode()

    full_data = header + data

    sha1 = hashlib.sha1(full_data).hexdigest()

    if write:
        # Répertoire .git/objects/<xx>/<yyyyyy...>
        obj_dir = os.path.join(git_dir, "objects", sha1[:2])
        obj_path = os.path.join(obj_dir, sha1[2:])


        compressed = zlib.compress(full_data)

        with open(obj_path, 'wb') as f:
            f.write(compressed)

    print(sha1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hash_object.py <file_path> [<git_dir>]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    git_dir = sys.argv[2] if len(sys.argv) > 2 else ".git"

    hash_object(file_path, git_dir)