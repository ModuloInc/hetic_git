import os
import shutil
import tempfile
import unittest
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.plumbing.hash_object import hash_object_data
from src.porcelain.ls_tree import ls_tree

class TestLsTree(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.git_dir = os.path.join(self.test_dir, ".mygit")
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)
        # Prepare tree content
        tree_content = "100644 file1.txt deadbeef\n100644 dir/file2.txt cafebabe\n"
        # Write tree object
        self.tree_sha = hash_object_data(tree_content, "tree", self.git_dir, write=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_ls_tree(self):
        captured = io.StringIO()
        sys.stdout = captured
        ls_tree(self.tree_sha, self.git_dir)
        sys.stdout = sys.__stdout__
        output = captured.getvalue().strip().split('\n')
        self.assertIn("100644 deadbeef file1.txt", output)
        self.assertIn("100644 cafebabe dir/file2.txt", output)
        self.assertEqual(len(output), 2)

    def test_ls_tree_not_a_tree(self):
        # Write a blob object
        blob_sha = hash_object_data("hello", "blob", self.git_dir, write=True)
        captured = io.StringIO()
        sys.stderr = captured
        with self.assertRaises(SystemExit):
            ls_tree(blob_sha, self.git_dir)
        sys.stderr = sys.__stderr__
        self.assertIn("is not a tree", captured.getvalue())

if __name__ == "__main__":
    unittest.main() 