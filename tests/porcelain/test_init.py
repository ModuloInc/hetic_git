import os
import shutil
import unittest
import tempfile
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.porcelain.init import init


class TestInit(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_init_creates_git_directory(self):
        init(self.test_dir)
        git_dir = os.path.join(self.test_dir, ".mygit")
        self.assertTrue(os.path.exists(git_dir),
                      "Le répertoire .git n'a pas été créé")

    def test_init_creates_required_subdirectories(self):
        init(self.test_dir)
        git_dir = os.path.join(self.test_dir, ".mygit")

        required_dirs = [
            os.path.join(git_dir, "objects"),
            os.path.join(git_dir, "refs"),
            os.path.join(git_dir, "refs/heads"),
            os.path.join(git_dir, "refs/tags"),
        ]

        for d in required_dirs:
            self.assertTrue(os.path.exists(d),
                          f"Le répertoire {d} n'a pas été créé")

    def test_init_creates_required_files(self):
        init(self.test_dir)
        git_dir = os.path.join(self.test_dir, ".mygit")

        required_files = [
            os.path.join(git_dir, "HEAD"),
            os.path.join(git_dir, "config"),
        ]

        for f in required_files:
            self.assertTrue(os.path.exists(f),
                          f"Le fichier {f} n'a pas été créé")

    def test_init_head_content(self):
        init(self.test_dir)
        head_path = os.path.join(self.test_dir, ".mygit", "HEAD")

        with open(head_path, 'r') as f:
            content = f.read().strip()

        self.assertEqual(content, "ref: refs/heads/main",
                        "Le fichier HEAD ne pointe pas vers refs/heads/main")

    def test_init_idempotent(self):
        result1 = init(self.test_dir)
        result2 = init(self.test_dir)

        self.assertTrue(result1, "Le premier appel à init a échoué")
        self.assertFalse(result2, "Le deuxième appel à init devrait retourner False")


if __name__ == "__main__":
    unittest.main()
