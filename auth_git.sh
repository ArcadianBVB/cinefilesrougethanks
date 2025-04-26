#!/bin/bash

echo "=== Initialisation de l'authentification GitHub via token ==="

# Étape 1 : Nettoyage lien distant
git remote set-url origin https://github.com/ArcadianBVB/cinefilesrougesuffer.git

# Étape 2 : Activer le stockage permanent des identifiants
git config --global credential.helper store

# Étape 3 : Forcer le premier push pour déclencher le prompt
echo ">>> Préparation à l'enregistrement du token..."
echo "Quand on te demande ton nom d'utilisateur GitHub : tape ArcadianBVB"
echo "Quand on te demande le mot de passe : colle ton token (ghp_...)"
echo

# Étape 4 : Déclenche le push de test
git push origin main

echo
echo ">>> Authentification enregistrée dans ~/.git-credentials"
echo ">>> Plus jamais de mot de passe à fournir pour tes futurs push !"
