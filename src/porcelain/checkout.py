import os
import sys
from src.porcelain.rev_parse import rev_parse
from src.porcelain.reset import reset

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")


def checkout(target, create_branch=None, git_dir=GIT_DIR, index_path=INDEX_FILE):
    head_path = os.path.join(git_dir, "HEAD")
    refs_heads_dir = os.path.join(git_dir, "refs", "heads")
    os.makedirs(refs_heads_dir, exist_ok=True)

    # If -b <branch> is specified, create a new branch pointing to current HEAD
    if create_branch:
        branch_ref = os.path.join(refs_heads_dir, create_branch)
        if os.path.exists(branch_ref):
            print(f"Erreur : la branche '{create_branch}' existe déjà.", file=sys.stderr)
            sys.exit(1)
        # Get current HEAD commit
        current_commit = rev_parse("HEAD", git_dir)
        with open(branch_ref, "w") as f:
            f.write(current_commit + "\n")
        # Now set target to the new branch
        target = create_branch

    # Resolve the target (branch name, tag, or SHA)
    commit_sha = rev_parse(target, git_dir)
    # Check if target is a branch
    branch_path = os.path.join(refs_heads_dir, target)
    if os.path.exists(branch_path):
        # Update HEAD to point to the branch
        with open(head_path, "w") as f:
            f.write(f"ref: refs/heads/{target}\n")
    else:
        # Detached HEAD
        with open(head_path, "w") as f:
            f.write(commit_sha + "\n")
    # Update index and working directory to match the commit
    reset(commit_sha, mode="hard", git_dir=git_dir, index_path=index_path)
    print(f"Switched to {'branch ' + target if os.path.exists(branch_path) else 'commit ' + commit_sha}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Switch to a branch or commit. Optionally create a new branch.")
    parser.add_argument("target", help="Nom de la branche ou SHA du commit à checkout")
    parser.add_argument("-b", dest="create_branch", help="Créer une nouvelle branche et la checkout", default=None)
    parser.add_argument("--git-dir", default=GIT_DIR, help="Chemin du dossier .mygit")
    args = parser.parse_args()
    checkout(args.target, create_branch=args.create_branch, git_dir=args.git_dir, index_path=os.path.join(args.git_dir, "index")) 