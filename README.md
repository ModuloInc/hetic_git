# Git from Scratch

A complete implementation of Git in Python, developed as part of a student project. This project recreates the main functionalities of Git with both porcelain (high-level) and plumbing (low-level) commands.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Project Installation

1. **Clone the project** (or download the files)
   ```bash
   cd /path/to/heticgit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the project in development mode**
   ```bash
   pip install -e .
   ```

   This installs the `mygit` package and makes the `mygit` command available globally.

### Installation Verification

```bash
mygit --help
```

## 📖 Usage

### Initialize a repository

```bash
mygit init [path]
```

Example:
```bash
mygit init my-project
cd my-project
```

### Main commands (Porcelain)

#### File management
```bash
# Add a file to the index
mygit add file.txt

# View repository status
mygit status

# List files in the index
mygit ls-files
```

#### Commits
```bash
# Create a commit
mygit commit -m "My commit message"

# View commit history
mygit log
```

#### Branches and navigation
```bash
# View all references (branches, tags)
mygit show-ref

# Resolve a reference to a SHA-1
mygit rev-parse HEAD
mygit rev-parse main

# Switch branch or commit
mygit checkout <branch-or-sha>

# Create a new branch and switch to it
mygit checkout -b new-branch
```

#### Advanced management
```bash
# Remove a file from index and working directory
mygit rm file.txt

# Remove a file from index only
mygit rm --cached file.txt

# Reset (soft/mixed/hard)
mygit reset --soft HEAD~1
mygit reset --mixed HEAD~1
mygit reset --hard HEAD~1

# Merge a branch
mygit merge other-branch
```

### Low-level commands (Plumbing)

#### Git objects
```bash
# Calculate file hash
mygit hash-object file.txt

# Calculate and write object to database
mygit hash-object -w file.txt

# Display object content
mygit cat-file -p <sha1>

# Display object type
mygit cat-file -t <sha1>
```

#### Trees and commits
```bash
# Write current index as tree object
mygit write-tree

# List tree content
mygit ls-tree <tree-sha>

# Create commit from tree
mygit commit-tree <tree-sha> -m "Message" [-p <parent-sha>]
```

## 🏗️ Project Structure

```
heticgit/
├── mygit/                 # Main CLI module
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py            # Command line interface
├── src/
│   ├── plumbing/         # Low-level commands
│   │   ├── cat_file.py
│   │   ├── commit_tree.py
│   │   ├── hash_object.py
│   │   └── write_tree.py
│   └── porcelain/        # High-level commands
│       ├── add.py
│       ├── checkout.py
│       ├── commit.py
│       ├── init.py
│       ├── log.py
│       ├── merge.py
│       ├── reset.py
│       ├── status.py
│       └── ...
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
├── setup.py             # Package configuration
└── README.md            # This file
```

## 🧪 Tests

To run tests:

```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python -m pytest tests/plumbing/
python -m pytest tests/porcelain/
```

## 🔧 Development

### Run in development mode

```bash
# Use Python module directly
python -m mygit --help

# Or use the installed command
mygit --help
```

### Comparison with Git

The project includes scripts to compare behavior with Git:

```bash
# Compare a specific command
./compare_git_mygit.sh

# Compare all commands
./compare_all_git_mygit.sh
```

## 📝 Implemented Features

- ✅ Repository initialization (`init`)
- ✅ Index management (`add`, `rm`, `ls-files`)
- ✅ Git objects (blobs, trees, commits)
- ✅ Commits (`commit`, `log`)
- ✅ Branches and references (`checkout`, `show-ref`, `rev-parse`)
- ✅ Reset (`reset --soft/mixed/hard`)
- ✅ Merge (`merge`)
- ✅ Repository status (`status`)
- ✅ Plumbing commands (`hash-object`, `cat-file`, `write-tree`, `commit-tree`)

## 🤝 Contributing

This project is developed in an educational context. To contribute:

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

Student project - HETIC

---

*This project is an educational implementation of Git and should not be used in production.*
