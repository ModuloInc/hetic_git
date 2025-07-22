#!/bin/bash
set -e

# Nettoyage
rm -rf /tmp/test_git /tmp/test_mygit
if [ -d "/tmp/test_git" ] || [ -d "/tmp/test_mygit" ]; then
    echo "Erreur : les dossiers temporaires n'ont pas été supprimés !" >&2
    exit 1
fi

# Création des dossiers de test
mkdir /tmp/test_git /tmp/test_mygit

# Initialisation des dépôts
git -C /tmp/test_git init
mygit init /tmp/test_mygit

# Ajout d'un fichier identique dans les deux dépôts
echo "Hello world" > /tmp/test_git/file.txt
cp /tmp/test_git/file.txt /tmp/test_mygit/file.txt

git -C /tmp/test_git add file.txt
git -C /tmp/test_git commit -m "Initial commit"

mygit add /tmp/test_mygit/file.txt
mygit commit -m "Initial commit"

# Comparaison des logs
GIT_LOG=$(git -C /tmp/test_git log --pretty=oneline)
MYGIT_LOG=$(mygit log | grep commit)

echo "--- git log ---"
echo "$GIT_LOG"
echo "--- mygit log ---"
echo "$MYGIT_LOG"

if [[ "$GIT_LOG" == *"$(echo $MYGIT_LOG | awk '{print $2}')"* ]]; then
    echo "[OK] Les messages de commit sont identiques."
else
    echo "[KO] Les messages de commit sont différents."
    exit 1
fi 