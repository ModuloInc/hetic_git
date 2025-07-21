import os
import shutil
import tempfile
import unittest
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.plumbing.commit_tree import commit_tree

class TestCommitTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.git_dir = os.path.join(self.test_dir, ".mygit")
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)
        # Créer un tree SHA bidon
        self.tree_sha = "a" * 40
        self.parent_sha = "b" * 40
        self.message = "Initial commit"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_commit_tree_no_parent(self):
        captured = io.StringIO()
        sys.stdout = captured
        oid = commit_tree(self.tree_sha, self.message, None, self.git_dir)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured.getvalue().strip(), oid)
        # Vérifie que l'objet a bien été écrit
        obj_path = os.path.join(self.git_dir, "objects", oid[:2], oid[2:])
        self.assertTrue(os.path.exists(obj_path))

    def test_commit_tree_with_parent(self):
        captured = io.StringIO()
        sys.stdout = captured
        oid = commit_tree(self.tree_sha, self.message, self.parent_sha, self.git_dir)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured.getvalue().strip(), oid)
        obj_path = os.path.join(self.git_dir, "objects", oid[:2], oid[2:])
        self.assertTrue(os.path.exists(obj_path))

if __name__ == "__main__":
    unittest.main() 