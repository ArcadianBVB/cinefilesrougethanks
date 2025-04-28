from flask import Blueprint, render_template, send_from_directory
import os

archives_bp = Blueprint('archives', __name__)

ARCHIVES_FOLDER = "archives"

@archives_bp.route("/archives")
def liste_archives():
    fichiers = []
    if os.path.exists(ARCHIVES_FOLDER):
        fichiers = [f for f in os.listdir(ARCHIVES_FOLDER) if f.endswith(".csv") or f.endswith(".zip")]
        fichiers.sort(reverse=True)  # Pour afficher les plus récents en haut
    return render_template("archives.html", fichiers=fichiers)

@archives_bp.route("/telecharger/<filename>")
def telecharger_archive(filename):
    return send_from_directory(ARCHIVES_FOLDER, filename, as_attachment=True)
