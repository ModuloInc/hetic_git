import os
import hashlib

# Chemin du dossier où on stocke les données Git
GIT_DIR = ".mygit"
# Chemin du fichier d'index qui référence les fichiers suivis
INDEX_FILE = os.path.join(GIT_DIR, "index")

def read_index():
    index = {}
    # Si le fichier d'index n'existe pas, on retourne un dictionnaire vide
    if not os.path.exists(INDEX_FILE):
        return index
    # On ouvre le fichier d'index en lecture
    with open(INDEX_FILE, "r") as f:
        for line in f:
            #On découpe chaque ligne en 3 parties : mode, nom du fichier, sha1
            parts = line.strip().split(" ")
            if len(parts) == 3:
                _, filename, sha1 = parts
                index[filename] = sha1
    # On retourne le dictionnaire avec {nom_fichier: sha1}
    return index

# Fonction qui calcule le hash (sha1) d'un fichier selon le format Git
def hash_file(path):
    with open(path, "rb") as f:
        data = f.read()
    # On ajoute un header comme Git ("blob <taille>\0") avant les données
    header = f"blob {len(data)}\0".encode()
    # On calcule le sha1 sur le header + les données
    return hashlib.sha1(header + data).hexdigest()

# Fonction principale qui affiche l'état du dépôt (comme "git status")
def status():
    index = read_index()  # On récupère les fichiers suivis (dans l'index)
    wd_files = []         # Liste des fichiers dans le working directory (le dossier courant)

    # On parcourt tous les fichiers du dossier courant (récursivement)
    for root, dirs, files in os.walk("."):
        # On ignore les dossiers cachés (sauf .mygit qui nous intéresse)
        dirs[:] = [d for d in dirs if not d.startswith(".") or d == ".mygit"]
        for f in files:
            # On ignore les fichiers cachés et ceux dans .mygit
            if f.startswith(".") or root.startswith("./.mygit"):
                continue
            full_path = os.path.relpath(os.path.join(root, f))
            wd_files.append(full_path)

    # Trois listes pour trier les fichiers selon leur statut
    staged = [] # fichiers suivis et prêts à être commit (inchangés)
    modified = [] # fichiers suivis mais modifiés depuis le dernier ajout à l'index
    untracked = [] # fichiers non suivis par Git

    # Pour chaque fichier de l'index
    for fname, sha1 in index.items():
        if not os.path.exists(fname):
            continue # Si le fichier a été supprimé du dossier, on l'ignore ici
        current_sha1 = hash_file(fname) # On calcule son sha1 actuel
        if current_sha1 == sha1:
            staged.append(fname) # Il est prêt à être commit (pas changé)
        else:
            modified.append(fname) # Il a été modifié depuis l'index

    # On cherche tous les fichiers qui sont dans le dossier mais pas dans l'index
    for fname in wd_files:
        if fname not in index:
            untracked.append(fname)

    # Affichage du statut selon les listes remplies
    if staged:
        print("Staged files (ready to commit):")
        for f in staged:
            print(f"  {f}")
    if modified:
        print("Modified files (not staged):")
        for f in modified:
            print(f"  {f}")
    if untracked:
        print("Untracked files:")
        for f in untracked:
            print(f"  {f}")
    # Si tout est vide, le dossier est "propre"
    if not (staged or modified or untracked):
        print("Nothing to commit, working tree clean.")

# Si on lance ce fichier directement, on exécute la commande status
if __name__ == "__main__":
    status()
