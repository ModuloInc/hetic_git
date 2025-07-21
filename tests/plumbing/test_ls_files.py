import os
import shutil
import tempfile
import unittest
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.plumbing.ls_files import ls_files

class TestLsFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.index_path = os.path.join(self.test_dir, "index")
        # Create a fake index file
        with open(self.index_path, 'w') as f:
            f.write("100644 file1.txt deadbeef\n")
            f.write("100644 dir/file2.txt cafebabe\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_ls_files(self):
        captured = io.StringIO()
        sys.stdout = captured
        ls_files(self.index_path)
        sys.stdout = sys.__stdout__
        output = captured.getvalue().strip().split('\n')
        self.assertIn("file1.txt", output)
        self.assertIn("dir/file2.txt", output)
        self.assertEqual(len(output), 2)

    def test_ls_files_missing_index(self):
        missing_path = os.path.join(self.test_dir, "noindex")
        captured = io.StringIO()
        sys.stderr = captured
        with self.assertRaises(SystemExit):
            ls_files(missing_path)
        sys.stderr = sys.__stderr__
        self.assertIn("Index file not found", captured.getvalue())

if __name__ == "__main__":
    unittest.main() 