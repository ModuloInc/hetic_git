import os
from src.porcelain.rev_parse import rev_parse
from src.plumbing.cat_file import read_object

def parse_commit(content):
    lines = content.decode().splitlines()
    commit_info = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('tree '):
            commit_info['tree'] = line[5:].strip()
        elif line.startswith('parent '):
            commit_info['parent'] = line[7:].strip()
        elif line.startswith('author '):
            commit_info['author'] = line[7:].strip()
        elif line.startswith('committer '):
            commit_info['committer'] = line[10:].strip()
        elif line.strip() == '':
            # The rest is the commit message
            commit_info['message'] = '\n'.join(lines[i+1:]).strip()
            break
        i += 1
    return commit_info

def log(git_dir='.mygit'):
    # Get HEAD commit SHA
    head_sha = rev_parse('HEAD', git_dir)
    if isinstance(head_sha, str):
        current = head_sha
    else:
        # rev_parse prints and returns, so if not string, try to read HEAD manually
        with open(os.path.join(git_dir, 'HEAD')) as f:
            ref = f.read().strip()
        if ref.startswith('ref: '):
            ref_path = os.path.join(git_dir, ref[5:].strip())
            with open(ref_path) as rf:
                current = rf.read().strip()
        else:
            current = ref
    while current:
        obj_type, content = read_object(current, git_dir)
        if obj_type != 'commit':
            print(f"Object {current} is not a commit.")
            break
        info = parse_commit(content)
        print(f"commit {current}")
        if 'author' in info:
            print(f"Author: {info['author']}")
        if 'committer' in info:
            print(f"Committer: {info['committer']}")
        print()
        print(f"    {info.get('message', '')}")
        print()
        parent = info.get('parent')
        if parent:
            current = parent
        else:
            break 