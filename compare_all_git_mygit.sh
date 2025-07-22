#!/bin/bash
set -e

# Nettoyage
tmpdir=/tmp/compare_git_mygit
rm -rf $tmpdir
if [ -d "$tmpdir" ]; then
    echo "Erreur : le dossier temporaire '$tmpdir' n'a pas été supprimé !" >&2
    exit 1
fi

gitdir=$tmpdir/git
git2dir=$tmpdir/git2
mygitdir=$tmpdir/mygit
mkdir -p $gitdir $git2dir $mygitdir

# INIT
echo "[TEST] init"
git -C $gitdir init > /dev/null
mygit init $mygitdir > /dev/null

# ADD & COMMIT
echo "[TEST] add & commit"
echo "Hello" > $gitdir/file.txt
cp $gitdir/file.txt $mygitdir/file.txt
git -C $gitdir add file.txt
git -C $gitdir commit -m "first" > /dev/null
(cd $mygitdir && mygit add file.txt > /dev/null)
(cd $mygitdir && mygit commit -m "first" > /dev/null)

# STATUS
echo "[TEST] status"
echo "change" >> $gitdir/file.txt
echo "change" >> $mygitdir/file.txt
git -C $gitdir status --short > $tmpdir/git_status.txt
(cd $mygitdir && mygit status) > $tmpdir/mygit_status.txt
diff $tmpdir/git_status.txt $tmpdir/mygit_status.txt || echo "[WARN] status diff"

# LOG
echo "[TEST] log"
git -C $gitdir log --pretty=oneline --no-color | cut -d' ' -f2- > $tmpdir/git_log.txt
(cd $mygitdir && mygit log | grep "message:" | cut -d' ' -f2-) > $tmpdir/mygit_log.txt
diff $tmpdir/git_log.txt $tmpdir/mygit_log.txt || echo "[WARN] log diff"

# CHECKOUT
echo "[TEST] checkout"
git -C $gitdir checkout -b newbranch > /dev/null
git -C $gitdir checkout main > /dev/null
(cd $mygitdir && mygit checkout -b newbranch > /dev/null)
(cd $mygitdir && mygit checkout main > /dev/null)

# MERGE
echo "[TEST] merge"
echo "other" > $git2dir/file.txt
git -C $git2dir init > /dev/null
git -C $git2dir add file.txt
git -C $git2dir commit -m "other" > /dev/null
git -C $gitdir remote add other $git2dir > /dev/null
git -C $gitdir fetch other > /dev/null
git -C $gitdir merge other/master > /dev/null || echo "[WARN] git merge failed"

# RM
echo "[TEST] rm"
echo "toremove" > $gitdir/toremove.txt
cp $gitdir/toremove.txt $mygitdir/toremove.txt
git -C $gitdir add toremove.txt
git -C $gitdir commit -m "add toremove" > /dev/null
git -C $gitdir rm toremove.txt > /dev/null
git -C $gitdir commit -m "rm toremove" > /dev/null
(cd $mygitdir && mygit add toremove.txt > /dev/null)
(cd $mygitdir && mygit commit -m "add toremove" > /dev/null)
(cd $mygitdir && mygit rm toremove.txt > /dev/null)
(cd $mygitdir && mygit commit -m "rm toremove" > /dev/null)

# RESET
echo "[TEST] reset"
git -C $gitdir reset --hard HEAD~1 > /dev/null
(cd $mygitdir && mygit reset --hard HEAD~1 > /dev/null)

# Résumé
echo "[INFO] Comparaison terminée. Vérifiez les [WARN] pour les différences." 