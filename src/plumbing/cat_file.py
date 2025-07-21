import sys
import os
import zlib
import hashlib

def get_object_path(oid, git_dir):
    return os.path.join(git_dir, "objects", oid[:2], oid[2:])

def read_object(oid, git_dir):
    obj_path = get_object_path(oid, git_dir)
    if not os.path.exists(obj_path):
        return None, None
    with open(obj_path, 'rb') as f:
        compressed = f.read()
    try:
        data = zlib.decompress(compressed)
    except zlib.error:
        return None, None
    header_end = data.find(b'\0')
    if header_end == -1:
        return None, None
    header = data[:header_end].decode()
    obj_type, size = header.split(' ')
    content = data[header_end+1:]
    return obj_type, content

def cat_file(oid, opt, git_dir):
    if opt not in ['-t', '-p']:
        print("Option invalide. Utilisez -t ou -p.", file=sys.stderr)
        sys.exit(1)
    obj_type, content = read_object(oid, git_dir)
    if obj_type is None:
        print(f"Erreur : OID '{oid}' introuvable ou corrompu.", file=sys.stderr)
        sys.exit(1)
    if opt == '-t':
        print(obj_type)
    elif opt == '-p':
        if obj_type == 'blob':
            try:
                print(content.decode(), end='')
            except UnicodeDecodeError:
                sys.stdout.buffer.write(content)
        else:
            print(content.decode(errors='replace'), end='')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cat_file.py -t|-p <oid> [<git_dir>]", file=sys.stderr)
        sys.exit(1)
    opt = sys.argv[1]
    oid = sys.argv[2]
    git_dir = ".mygit"
    cat_file(oid, opt, git_dir) 