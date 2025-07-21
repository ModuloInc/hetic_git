import os
import sys
from src.plumbing.rev_parse import rev_parse
from src.plumbing.cat_file import read_object

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")

# Utilitaire pour parser un commit (repris de log.py)
def parse_commit(content):
    lines = content.decode().splitlines()
    commit_info = {}
    for line in lines:
        if line.startswith('tree '):
            commit_info['tree'] = line[5:].strip()
        elif line.startswith('parent '):
            commit_info['parent'] = line[7:].strip()
        elif line.startswith('author '):
            commit_info['author'] = line[7:].strip()
        elif line.startswith('committer '):
            commit_info['committer'] = line[10:].strip()
        elif line.strip() == '':
            break
    return commit_info

def reset(commit_ref, mode="mixed", git_dir=GIT_DIR, index_path=INDEX_FILE):
    # 1. Résoudre le commit
    commit_sha = rev_parse(commit_ref, git_dir)
    if not isinstance(commit_sha, str):
        # rev_parse peut print et return None
        print(f"Impossible de résoudre {commit_ref}", file=sys.stderr)
        sys.exit(1)
    # 2. Lire l'objet commit
    obj_type, commit_content = read_object(commit_sha, git_dir)
    if obj_type != "commit":
        print(f"{commit_sha} n'est pas un commit.", file=sys.stderr)
        sys.exit(1)
    commit_info = parse_commit(commit_content)
    tree_sha = commit_info["tree"]
    # 3. --soft: déplacer HEAD
    # HEAD peut pointer vers une ref ou contenir le SHA directement
    head_path = os.path.join(git_dir, "HEAD")
    with open(head_path) as f:
        head_content = f.read().strip()
    if head_content.startswith("ref: "):
        ref_rel = head_content[5:].strip()
        ref_path = os.path.join(git_dir, ref_rel)
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        with open(ref_path, "w") as rf:
            rf.write(commit_sha + "\n")
    else:
        with open(head_path, "w") as f:
            f.write(commit_sha + "\n")
    if mode == "soft":
        print(f"HEAD déplacé vers {commit_sha}")
        return
    # 4. --mixed: réinitialiser l'index
    obj_type, tree_content = read_object(tree_sha, git_dir)
    if obj_type != "tree":
        print(f"{tree_sha} n'est pas un tree.", file=sys.stderr)
        sys.exit(1)
    # On écrase l'index avec le contenu du tree
    with open(index_path, "w") as idx:
        for line in tree_content.decode().splitlines():
            parts = line.strip().split()
            if len(parts) == 3:
                mode, path, sha1 = parts
                idx.write(f"{mode} {path} {sha1}\n")
    if mode == "mixed":
        print(f"Index réinitialisé sur {tree_sha}")
        return
    # 5. --hard: réinitialiser le working directory
    for line in tree_content.decode().splitlines():
        parts = line.strip().split()
        if len(parts) == 3:
            mode, path, sha1 = parts
            obj_type, blob_content = read_object(sha1, git_dir)
            if obj_type != "blob":
                continue
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(blob_content)
    print(f"Working directory réinitialisé sur {tree_sha}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reset HEAD, index, and working directory to a given commit.")
    parser.add_argument("commit_ref", help="Référence du commit (SHA, HEAD, branche, etc.)")
    parser.add_argument("--soft", action="store_true", help="Déplacer HEAD seulement")
    parser.add_argument("--mixed", action="store_true", help="Déplacer HEAD et réinitialiser l'index (défaut)")
    parser.add_argument("--hard", action="store_true", help="Déplacer HEAD, réinitialiser l'index et le working directory")
    parser.add_argument("--git-dir", default=GIT_DIR, help="Chemin du dossier .mygit")
    args = parser.parse_args()
    if args.soft:
        mode = "soft"
    elif args.hard:
        mode = "hard"
    else:
        mode = "mixed"
    reset(args.commit_ref, mode=mode, git_dir=args.git_dir, index_path=os.path.join(args.git_dir, "index")) 