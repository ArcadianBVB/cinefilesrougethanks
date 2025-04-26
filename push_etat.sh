#!/bin/bash

if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo ">>> Erreur : tu n'es pas dans un projet Git."
  exit 1
fi

commit_id=$(git rev-parse HEAD)
commit_msg=$(git log -1 --pretty=format:"%s")

echo ">>> Dernier commit :"
echo "ID    : $commit_id"
echo "Msg   : $commit_msg"
echo ">>> Tentative de push vers origin/main..."

git push origin main

echo ">>> Push terminé."
