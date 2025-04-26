from flask import Blueprint, render_template, request
import sqlite3
import csv
import os
import zipfile
from datetime import datetime

exporter_mois_bp = Blueprint('exporter_mois', __name__)

DB_NAME = "stock.db"

@exporter_mois_bp.route("/exporter_proformas_par_mois", methods=["GET", "POST"])
def exporter_proformas_par_mois():
    if request.method == "POST":
        annee = request.form.get("annee")
        mois = request.form.get("mois")

        if not annee or not mois:
            return "Erreur : Veuillez choisir une année et un mois."

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Correction ici pour bien extraire l'année et le mois
        c.execute("""
            SELECT * FROM proformas_payes 
            WHERE strftime('%Y', date_commande) = ? 
            AND strftime('%m', date_commande) = ?
        """, (annee, mois))
        
        proformas = c.fetchall()
        conn.close()

        if not proformas:
            return f"Aucun proforma trouvé pour {mois}/{annee}."

        os.makedirs("archives", exist_ok=True)
        date_now = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"archives/proformas_payes_{annee}_{mois}_{date_now}.csv"
        zip_filename = f"archives/proformas_payes_{annee}_{mois}_{date_now}.zip"

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([col for col in proformas[0].keys()])
            for row in proformas:
                writer.writerow([row[col] for col in row.keys()])

        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_filename)

        return f"Export terminé pour {mois}/{annee}. Fichier CSV + ZIP créé."

    return render_template("exporter_mois_proformas_payes.html")
