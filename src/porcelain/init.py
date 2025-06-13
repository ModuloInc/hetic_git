import os
import sys

def init(directory="."):
    git_dir = os.path.join(directory, ".mygit")

    if os.path.exists(git_dir):
        print(f"Le dépôt Git est déjà initialisé dans {os.path.abspath(directory)}")
        return False

    try:
        dirs = [
            git_dir,
            os.path.join(git_dir, "objects"),
            os.path.join(git_dir, "refs"),
            os.path.join(git_dir, "refs/heads"),
            os.path.join(git_dir, "refs/tags"),
        ]

        for d in dirs:
            os.makedirs(d)

        with open(os.path.join(git_dir, "HEAD"), "w") as f:
            f.write("ref: refs/heads/main\n")

        with open(os.path.join(git_dir, "config"), "w") as f:
            f.write("[core]\n")
            f.write("\trepositoryformatversion = 0\n")
            f.write("\tfilemode = true\n")
            f.write("\tbare = false\n")

        print(f"Dépôt Git initialisé dans {os.path.abspath(directory)}")
        return True

    except Exception as e:
        print(f"Erreur lors de l'initialisation du dépôt Git : {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    target_dir = "."
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]

    init(target_dir)
