#!/bin/bash

echo "=== Configuration auto du push Git vers GitHub ==="
read -p "Ton token GitHub (ghp_...): " token
read -p "Nom exact du dépôt GitHub (ex: cinefilesrougesuffer): " repo

# Vérifie que tu es dans un repo Git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Erreur : tu n'es pas dans un projet Git."
  exit 1
fi

# Configure le lien distant avec le token
url="https://$token@github.com/ArcadianBVB/$repo.git"
git remote set-url origin "$url"

echo "Lien distant mis à jour :"
git remote -v

echo ">>> Test de push..."
git push origin main
