import os
import sys
from src.porcelain.rev_parse import rev_parse
from src.porcelain.reset import reset

GIT_DIR = ".mygit"
INDEX_FILE = os.path.join(GIT_DIR, "index")


def checkout(target, create_branch=None, git_dir=GIT_DIR, index_path=INDEX_FILE):
    """
    Switch to a branch or commit. Optionally create a new branch.
    Args:
        target (str): Branch name or commit SHA to checkout.
        create_branch (str, optional): Name of new branch to create and checkout.
        git_dir (str): Path to the .mygit directory.
        index_path (str): Path to the index file.
    """
    head_path = os.path.join(git_dir, "HEAD")
    refs_heads_dir = os.path.join(git_dir, "refs", "heads")
    os.makedirs(refs_heads_dir, exist_ok=True)

    # If -b <branch> is specified, create a new branch pointing to current HEAD
    if create_branch:
        branch_ref = os.path.join(refs_heads_dir, create_branch)
        if os.path.exists(branch_ref):
            print(f"Error: branch '{create_branch}' already exists.", file=sys.stderr)
            sys.exit(1)
        # Get current HEAD commit
        current_commit = rev_parse("HEAD", git_dir)
        with open(branch_ref, "w") as f:
            f.write(current_commit + "\n")
        # Now set target to the new branch
        target = create_branch

    # Resolve the target (branch name, tag, or SHA)
    branch_path = os.path.join(refs_heads_dir, target)
    if os.path.exists(branch_path):
        commit_sha = rev_parse(target, git_dir)
        # Update HEAD to point to the branch
        with open(head_path, "w") as f:
            f.write(f"ref: refs/heads/{target}\n")
        # Update index and working directory to match the commit
        reset(commit_sha, mode="hard", git_dir=git_dir, index_path=index_path)
        print(f"Switched to branch {target}")
    else:
        print(f"Error: reference '{target}' not found.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Switch to a branch or commit. Optionally create a new branch.")
    parser.add_argument("target", help="Branch name or commit SHA to checkout")
    parser.add_argument("-b", dest="create_branch", help="Create a new branch and check it out", default=None)
    parser.add_argument("--git-dir", default=GIT_DIR, help="Path to the .mygit directory")
    args = parser.parse_args()
    checkout(args.target, create_branch=args.create_branch, git_dir=args.git_dir, index_path=os.path.join(args.git_dir, "index")) 