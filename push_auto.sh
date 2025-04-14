#!/data/data/com.termux/files/usr/bin/bash

# Demander à l’utilisateur de nommer l’état
read -p "Nom de l’état à enregistrer (ex: T3, cinefilesrouge_avril, backup_nuit) : " nom_etat

# Générer la date et l’heure actuelles
horodatage=$(date +"%Y-%m-%d à %Hh%M")

# Construire le message de commit
message="[$nom_etat] - sauvegarde du $horodatage"

# Lancer les commandes Git
git add .
git commit -m "$message"
git push origin main
