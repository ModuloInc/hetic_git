# 1. Nettoyer l'ancien répertoire de test et en créer un nouveau
rm -rf monrepo
python3 mygit/cli.py init monrepo
cd monrepo

# 2. Créer un premier fichier sur la branche 'main'
echo "Contenu initial" > fichier1.txt
python3 ../mygit/cli.py add fichier1.txt
python3 ../mygit/cli.py commit -m "Commit initial sur main"

# 3. Créer une nouvelle branche 'feature' et basculer dessus
python3 ../mygit/cli.py checkout -b feature

# 4. Créer un nouveau fichier sur la branche 'feature'
echo "Nouveau fichier sur feature" > fichier2.txt
python3 ../mygit/cli.py add fichier2.txt
python3 ../mygit/cli.py commit -m "Ajout de fichier2 sur feature"

# 5. Revenir sur la branche 'main'
python3 ../mygit/cli.py checkout main

# 6. Modifier le premier fichier sur 'main' pour créer une divergence
echo "Modification sur main" > fichier1.txt
python3 ../mygit/cli.py add fichier1.txt
python3 ../mygit/cli.py commit -m "Modification de fichier1 sur main"

# 7. Lancer la fusion de 'feature' dans 'main'
python3 ../mygit/cli.py merge feature;

# (Assurez-vous d'être dans le répertoire /Users/anthonyzhao/Developer/Projet fil rouge/heticgit)
# 1. Nettoyer et réinitialiser le répertoire
cd ..
rm -rf monrepo
python3 mygit/cli.py init monrepo
cd monrepo

# 2. Créer un fichier de base
echo "Ligne originale" > conflit.txt
python3 ../mygit/cli.py add conflit.txt
python3 ../mygit/cli.py commit -m "Commit initial"

# 3. Créer une branche 'feature-conflit'
python3 ../mygit/cli.py checkout -b feature-conflit

# 4. Modifier le fichier sur la nouvelle branche
echo "Changement sur la branche feature" > conflit.txt
python3 ../mygit/cli.py add conflit.txt
python3 ../mygit/cli.py commit -m "Modification sur feature-conflit"

# 5. Revenir sur 'main' et modifier le même fichier
python3 ../mygit/cli.py checkout main
echo "Changement sur la branche main" > conflit.txt
python3 ../mygit/cli.py add conflit.txt
python3 ../mygit/cli.py commit -m "Modification sur main"

# 6. Tenter la fusion qui devrait provoquer un conflit
python3 ../mygit/cli.py merge feature-conflit