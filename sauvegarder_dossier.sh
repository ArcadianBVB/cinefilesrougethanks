#!/bin/bash

echo "=== Sauvegarde cohérente du projet en dossier ==="

DATE=$(date +%Y-%m-%d_%Hh%M)
DESTINATION="/storage/emulated/0/Download/backup_cinefiles/backup_$DATE/"

mkdir -p "$DESTINATION"
cp -r ~/cinefilesrouge "$DESTINATION"

echo "=== Sauvegarde terminée dans : $DESTINATION ==="
