from flask import Blueprint, render_template, request, send_file, redirect, url_for
import sqlite3
import csv
import os
import zipfile
from datetime import datetime

exporter_bp = Blueprint('exporter', __name__)

DB_NAME = "stock.db"

@exporter_bp.route("/exporter_proformas_par_annee", methods=["GET", "POST"])
def exporter_proformas_par_annee():
    if request.method == "POST":
        annee = request.form.get("annee")
        if not annee:
            return "Erreur : Veuillez sélectionner une année."

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM proformas_payes WHERE annee = ?", (annee,))
        proformas = c.fetchall()
        conn.close()

        if not proformas:
            return f"Aucun proforma payé trouvé pour l'année {annee}."

        os.makedirs("archives", exist_ok=True)
        date_now = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"archives/proformas_payes_{annee}_{date_now}.csv"
        zip_filename = f"archives/proformas_payes_{annee}_{date_now}.zip"

        with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([col for col in proformas[0].keys()])
            for row in proformas:
                writer.writerow([row[col] for col in row.keys()])

        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_filename)

        return render_template("confirmer_suppression.html", annee=annee)

    return render_template("exporter_supprimer_proformas_payes.html")


@exporter_bp.route("/confirmer_suppression_proformas/<annee>", methods=["POST"])
def confirmer_suppression_proformas(annee):
    action = request.form.get("action")
    if action == "supprimer":
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM proformas_payes WHERE annee = ?", (annee,))
        conn.commit()
        conn.close()
        return f"Les proformas payés de l'année {annee} ont été supprimés avec succès."
    else:
        return redirect(url_for('commandes.proformas_payes'))
