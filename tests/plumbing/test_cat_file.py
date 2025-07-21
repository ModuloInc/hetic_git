import os
import shutil
import tempfile
import unittest
import sys
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.plumbing.hash_object import hash_object
from src.plumbing.cat_file import cat_file

class TestCatFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.git_dir = os.path.join(self.test_dir, ".mygit")
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)
        # Créer un fichier de test
        self.file_path = os.path.join(self.test_dir, "test.txt")
        with open(self.file_path, 'w') as f:
            f.write("hello world\n")
        # Ajouter le blob
        self.oid = hash_object(self.file_path, self.git_dir, write=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_cat_file_type(self):
        captured = io.StringIO()
        sys.stdout = captured
        cat_file(self.oid, '-t', self.git_dir)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured.getvalue().strip(), 'blob')

    def test_cat_file_pretty_print(self):
        captured = io.StringIO()
        sys.stdout = captured
        cat_file(self.oid, '-p', self.git_dir)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured.getvalue(), 'hello world\n')

    def test_cat_file_invalid_oid(self):
        captured = io.StringIO()
        sys.stderr = captured
        with self.assertRaises(SystemExit):
            cat_file('deadbeefdeadbeefdeadbeefdeadbeefdeadbeef', '-t', self.git_dir)
        sys.stderr = sys.__stderr__
        self.assertIn("Erreur", captured.getvalue())

    def test_cat_file_invalid_option(self):
        captured = io.StringIO()
        sys.stderr = captured
        with self.assertRaises(SystemExit):
            cat_file(self.oid, '--invalid', self.git_dir)
        sys.stderr = sys.__stderr__
        self.assertIn("Option invalide", captured.getvalue())

if __name__ == "__main__":
    unittest.main() 