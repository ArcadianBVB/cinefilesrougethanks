#!/bin/bash

echo "=== Configuration automatique du push GitHub ==="
read -p "Nom du dépôt GitHub (ex: cinefilesrougesuffer) : " repo
read -p "Ton token GitHub (ex: github_pat_11BRC...) : " token

# Vérifie que tu es bien dans un projet git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Tu n'es pas dans un dossier Git valide."
  exit 1
fi

# Construction de l'URL complète avec token
url="https://$token@github.com/ArcadianBVB/$repo.git"

# Mise à jour du remote
git remote set-url origin "$url"

# Affiche les infos pour vérification
echo "URL Git configurée : $url"
git remote -v

# Push direct
echo ">>> Push en cours..."
git push origin main

echo
echo ">>> Terminé. Si pas d’erreur, plus besoin de refaire cette étape."
