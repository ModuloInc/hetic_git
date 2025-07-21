# python
import os
import hashlib

GIT_DIR = ".git"
INDEX_FILE = os.path.join(GIT_DIR, "index")

def read_index():
    """Lit l'index et retourne un dict {filename: hash}"""
    index = {}
    if not os.path.exists(INDEX_FILE):
        return index
    with open(INDEX_FILE, "r") as f:
        for line in f:
            filename, sha1 = line.strip().split(" ")
            index[filename] = sha1
    return index

def hash_file(path):
    """Calcule le hash SHA-1 d'un fichier"""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def get_working_files():
    """Liste tous les fichiers du répertoire de travail (hors .git)"""
    files = []
    for root, dirs, filenames in os.walk("."):
        if GIT_DIR in dirs:
            dirs.remove(GIT_DIR)
        for name in filenames:
            files.append(os.path.relpath(os.path.join(root, name), "."))
    return files

def run():
    index = read_index()
    work_files = get_working_files()

    staged = []
    modified = []
    deleted = []
    untracked = []

    # Fichiers dans l'index
    for fname, idx_hash in index.items():
        if fname in work_files:
            work_hash = hash_file(fname)
            if work_hash == idx_hash:
                staged.append(fname)
            else:
                modified.append(fname)
        else:
            deleted.append(fname)

    # Fichiers non suivis
    for fname in work_files:
        if fname not in index:
            untracked.append(fname)

    # Affichage complexe
    print("Fichiers stagés :")
    for f in staged:
        print(f"  {f}")

    print("\nFichiers modifiés (non stagés) :")
    for f in modified:
        print(f"  {f}")

    print("\nFichiers supprimés (index mais pas dans le travail) :")
    for f in deleted:
        print(f"  {f}")

    print("\nFichiers non suivis :")
    for f in untracked:
        print(f"  {f}")

# Exemple de résultat complexe :
# Fichiers stagés :
#   src/main.py
#   README.md
#
# Fichiers modifiés (non stagés) :
#   src/utils.py
#
# Fichiers supprimés (index mais pas dans le travail) :
#   docs/old_doc.md
#
# Fichiers non suivis :
#   notes.txt
#   test/test_status.py