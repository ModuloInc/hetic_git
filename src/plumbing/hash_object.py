import sys
import os
import hashlib
import zlib


def hash_object(file_path, git_dir=".mygit", write=False):
    """
    Compute the SHA-1 hash of a file and optionally write it as a Git object.
    Args:
        file_path (str): Path to the file to hash.
        git_dir (str): Path to the .mygit directory.
        write (bool): If True, write the object to the Git database.
    Returns:
        str: The SHA-1 hash of the object.
    """
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' not found or is not a file.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'rb') as f:
        data = f.read()

    header = f"blob {len(data)}\0".encode()

    full_data = header + data

    sha1 = hashlib.sha1(full_data).hexdigest()

    if write:
        # .git/objects/<xx>/<yyyyyy...>
        obj_dir = os.path.join(git_dir, "objects", sha1[:2])
        obj_path = os.path.join(obj_dir, sha1[2:])

        os.makedirs(obj_dir, exist_ok=True)

        compressed = zlib.compress(full_data)

        with open(obj_path, 'wb') as f:
            f.write(compressed)

    print(sha1)
    return sha1

def hash_object_data(data, obj_type, git_dir=".mygit", write=False):
    """
    Compute the SHA-1 hash of raw data and optionally write it as a Git object.
    Args:
        data (str or bytes): Data to hash.
        obj_type (str): Type of the object (e.g., 'tree', 'blob').
        git_dir (str): Path to the .mygit directory.
        write (bool): If True, write the object to the Git database.
    Returns:
        str: The SHA-1 hash of the object.
    """
    if isinstance(data, str):
        data = data.encode()
    header = f"{obj_type} {len(data)}\0".encode()
    full_data = header + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    if write:
        obj_dir = os.path.join(git_dir, "objects", sha1[:2])
        obj_path = os.path.join(obj_dir, sha1[2:])
        os.makedirs(obj_dir, exist_ok=True)
        compressed = zlib.compress(full_data)
        with open(obj_path, 'wb') as f:
            f.write(compressed)
    print(sha1)
    return sha1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hash_object.py <file_path> [<git_dir>]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    git_dir = sys.argv[2] if len(sys.argv) > 2 else ".mygit"

    hash_object(file_path, git_dir)