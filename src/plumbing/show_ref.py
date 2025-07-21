import os

def show_ref(git_dir=".mygit"):
    refs_dir = os.path.join(git_dir, "refs")
    for ref_type in ["heads", "tags"]:
        ref_path = os.path.join(refs_dir, ref_type)
        if not os.path.isdir(ref_path):
            continue
        for ref_name in os.listdir(ref_path):
            full_ref = f"refs/{ref_type}/{ref_name}"
            ref_file = os.path.join(ref_path, ref_name)
            try:
                with open(ref_file, "r") as f:
                    sha = f.read().strip()
                print(f"{sha} {full_ref}")
            except Exception:
                continue

if __name__ == "__main__":
    import sys
    git_dir = sys.argv[1] if len(sys.argv) > 1 else ".mygit"
    show_ref(git_dir) 