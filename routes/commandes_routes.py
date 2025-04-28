from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import random
from flask import make_response
from collections import defaultdict
from datetime import datetime
from fpdf import FPDF
from flask import send_file
import csv, os, zipfile
import string
import json
from base_price import calculer_prix

commandes_bp = Blueprint('commandes', __name__)
DB_NAME = "stock.db"

# Fonction de pagination copiée depuis stock_routes
def get_pagination_links(page, total_pages, delta=2):
    links = []
    for p in range(1, total_pages + 1):
        if p == 1 or p == total_pages or (p >= page - delta and p <= page + delta):
            links.append(p)
        elif links[-1] != "...":
            links.append("...")
    return links

@commandes_bp.route("/view/<int:proforma_id>")
def view_proforma(proforma_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proformas WHERE id=?", (proforma_id,))
    proforma = c.fetchone()
    conn.close()

    if not proforma:
        return "Commande non trouvée", 404

    try:
        produits = json.loads(proforma["produits"])
    except:
        produits = []

    return render_template("proforma_view.html", proforma=proforma, produits=produits)

commandes_bp = Blueprint('commandes', __name__)
DB_NAME = "stock.db"

def generate_order_id():
    # Génère un ID unique au format "IDYYYYMMDDXXXX"
    date_str = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    order_id = f"ID{date_str}{random_str}"
    print("Generated Order ID:", order_id)
    return order_id

@commandes_bp.route("/commandes/payes")
def proformas_payes():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proformas_payes ORDER BY id ASC")
    proformas = c.fetchall()
    conn.close()

    liste_proformas = []
    for row in proformas:
        try:
            date_obj = datetime.strptime(row["date_generation"], "%Y-%m-%d %H:%M:%S")
            annee = str(date_obj.year)
            mois = date_obj.strftime("%B")  # Avril, Mai...
            jour = str(date_obj.day)
            jour_semaine = date_obj.strftime("%A")  # Lundi, Mardi...
        except:
            annee = ""
            mois = ""
            jour = ""
            jour_semaine = ""

        liste_proformas.append({
            "id_commande": row["id_commande"],
            "nom_client": row["nom_client"],
            "contact": row["contact"],
            "type_client": row["type_client"],
            "produits": row["produits"],
            "montant_total": row["montant_total"],
            "mode_livraison": row["mode_livraison"],
            "frais_livraison": row["frais_livraison"],
            "observations": row["observations"],
            "date_commande": row["date_commande"],
            "date_generation": row["date_generation"],
            "date_expiration": row["date_expiration"],
            "statut": row["statut"],
            "annee": annee,
            "mois": mois,
            "jour": jour,
            "jour_semaine": jour_semaine
        })

    return render_template("commandes_payes.html", proformas=liste_proformas)

@commandes_bp.route("/nouvelle", methods=["GET", "POST"])
def nouvelle_commande():
    if request.method == "POST":
        nom_client = request.form.get("nom_client")
        contact = request.form.get("contact")
        type_client = request.form.get("type_client")
        produits_json = request.form.get("produits_json")  # Liste de produits en JSON
        montant_total = request.form.get("montant_total")  # Ce champ est calculé côté JS
        mode_livraison = request.form.get("mode_livraison")
        frais_livraison = request.form.get("frais_livraison")
        observations = request.form.get("observations")
        date_commande = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_generation = date_commande
        date_expiration = (datetime.now() + timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
        statut = "En attente"
        id_commande = generate_order_id()

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO proformas (
                id_commande,
                nom_client,
                contact,
                type_client,
                produits,
                montant_total,
                mode_livraison,
                frais_livraison,
                observations,
                date_commande,
                date_generation,
                date_expiration,
                statut,
                chemin_fichier
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            id_commande,
            nom_client,
            contact,
            type_client,
            produits_json,
            montant_total,
            mode_livraison,
            frais_livraison,
            observations,
            date_commande,
            date_generation,
            date_expiration,
            statut,
            ""
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("commandes.liste_commandes"))
    return render_template("nouvelle_commande.html")

@commandes_bp.route("/generer_pdf/<int:proforma_id>")
def generer_pdf(proforma_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proformas WHERE id=?", (proforma_id,))
    proforma = c.fetchone()
    conn.close()

    if not proforma:
        return "Commande introuvable", 404

    try:
        produits = json.loads(proforma["produits"])
    except:
        produits = []

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, "Fiche Proforma", ln=True, align="C")
    pdf.ln(10)

    infos = [
        ("ID Commande", proforma["id_commande"]),
        ("Nom client", proforma["nom_client"]),
        ("Contact", proforma["contact"]),
        ("Type client", proforma["type_client"]),
        ("Livraison", proforma["mode_livraison"]),
        ("Frais", f"{proforma['frais_livraison']} $"),
        ("Observations", proforma["observations"]),
        ("Date commande", proforma["date_commande"]),
        ("Expiration", proforma["date_expiration"]),
        ("Statut", proforma["statut"]),
    ]
    for label, val in infos:
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(50, 10, f"{label} :", ln=0)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, str(val))

    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Produits :", ln=True)

    pdf.set_font("Arial", size=12)
    for p in produits:
        ligne = f"{p['titre']} ({p['qualite']}) - {p['quantite']} x {p['prix']} $ = {p['total']} $"
        pdf.multi_cell(0, 10, ligne)

    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, f"Total : {proforma['montant_total']} $", ln=True)

    response = make_response(pdf.output(dest="S").encode("latin1"))
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=proforma_{proforma_id}.pdf"
    return response

@commandes_bp.route("/liste")
def liste_commandes():
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    per_page = 11
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM proformas")
    total = c.fetchone()[0]
    total_pages = (total + per_page - 1) // per_page

    c.execute("SELECT * FROM proformas ORDER BY id ASC LIMIT ? OFFSET ?", (per_page, offset))
    commandes = c.fetchall()
    conn.close()

    commandes_formatees = []
    for cmd in commandes:
        try:
            produits = json.loads(cmd["produits"])
        except:
            produits = []
        commandes_formatees.append({
            "id": cmd["id"],  # utilisé pour action/modif/suppression
            "id_commande": cmd["id_commande"],  # utilisé pour affichage
            "nom_client": cmd["nom_client"],
            "contact": cmd["contact"],
            "type_client": cmd["type_client"],
            "produits": produits,
            "montant_total": cmd["montant_total"],
            "statut": cmd["statut"],
            "mode_livraison": cmd["mode_livraison"],
            "frais_livraison": cmd["frais_livraison"],
            "date_generation": cmd["date_generation"]
        })

    pagination_links = get_pagination_links(page, total_pages, delta=2)

    return render_template("commandes_liste.html",
                           commandes=commandes_formatees,
                           page=page,
                           total_pages=total_pages,
                           pagination_links=pagination_links,
                           per_page=per_page)

@commandes_bp.route("/nettoyer", methods=["GET"])
def lancer_nettoyage_manuel():
    import subprocess
    subprocess.run(["python", "nettoyage_proformas.py"])
    return redirect(url_for('commandes.liste_commandes'))

@commandes_bp.route("/search_products")
def search_products():
    query = request.args.get('q', '')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT titre, prix, qualite FROM stock WHERE titre LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return jsonify([{'titre': r[0], 'prix': r[1], 'qualite': r[2]} for r in results])

@commandes_bp.route("/view/<int:proforma_id>")
def view_proforma(proforma_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proformas WHERE id=?", (proforma_id,))
    proforma = c.fetchone()
    conn.close()

    if not proforma:
        return "Commande non trouvée", 404

    try:
        produits = json.loads(proforma["produits"])
    except:
        produits = []

    return render_template("proforma_view.html", proforma=proforma, produits=produits)

@commandes_bp.route("/delete/<int:proforma_id>")
def supprimer_commande(proforma_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM proformas WHERE id=?", (proforma_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("commandes.liste_commandes"))

@commandes_bp.route("/changer_statut/<int:proforma_id>/<string:nouveau_statut>")
def changer_statut(proforma_id, nouveau_statut):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE proformas SET statut=? WHERE id=?", (nouveau_statut, proforma_id))
    conn.commit()
    conn.close()
    return redirect(url_for("commandes.liste_commandes"))

@commandes_bp.route("/modifier/<int:proforma_id>", methods=["GET", "POST"])
def modifier_commande(proforma_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == "POST":
        nom_client = request.form.get("nom_client")
        contact = request.form.get("contact")
        type_client = request.form.get("type_client")
        mode_livraison = request.form.get("mode_livraison")
        observations = request.form.get("observations")
        statut = request.form.get("statut")

        c.execute("""
            UPDATE proformas SET 
                nom_client = ?, 
                contact = ?, 
                type_client = ?, 
                mode_livraison = ?, 
                observations = ?, 
                statut = ?
            WHERE id = ?
        """, (nom_client, contact, type_client, mode_livraison, observations, statut, proforma_id))
        conn.commit()
        conn.close()
        return redirect(url_for('commandes.liste_commandes'))

    # GET : charger les données
    c.execute("SELECT * FROM proformas WHERE id=?", (proforma_id,))
    proforma = c.fetchone()
    conn.close()

    if not proforma:
        return "Commande non trouvée", 404

    return render_template("modifier_commande.html", proforma=proforma)

@commandes_bp.route("/rechercher", methods=["GET"])
def rechercher_commandes():
    nom_client = request.args.get("nom_client", "").lower()
    id_commande = request.args.get("id_commande", "").strip()
    statut = request.args.get("statut", "")
    date_debut = request.args.get("date_debut", "")
    date_fin = request.args.get("date_fin", "")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM proformas ORDER BY id ASC")
    resultats = c.fetchall()
    conn.close()

    commandes_formatees = []
    for cmd in resultats:
        try:
            produits = json.loads(cmd["produits"])
        except:
            produits = []

        # Filtres actifs
        if nom_client and nom_client not in cmd["nom_client"].lower():
            continue
        if id_commande and id_commande.lower() not in cmd["id_commande"].lower():
            continue
        if statut and statut != cmd["statut"]:
            continue
        if date_debut and cmd["date_generation"] < date_debut:
            continue
        if date_fin and cmd["date_generation"] > date_fin:
            continue

        commandes_formatees.append({
            "id": cmd["id"],
            "id_commande": cmd["id_commande"],
            "nom_client": cmd["nom_client"],
            "contact": cmd["contact"],
            "type_client": cmd["type_client"],
            "produits": produits,
            "montant_total": cmd["montant_total"],
            "statut": cmd["statut"],
            "mode_livraison": cmd["mode_livraison"],
            "frais_livraison": cmd["frais_livraison"],
            "date_generation": cmd["date_generation"]
        })

    return render_template("commandes_liste.html",
                           commandes=commandes_formatees,
                           page=1,
                           total_pages=1,
                           pagination_links=[],
                           per_page=len(commandes_formatees))

@commandes_bp.route("/archiver_proformas_payes")
def archiver_proformas_payes():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Sélection des proformas payés vieux de plus d’un an
    c.execute("""
        SELECT * FROM proformas_payes
        WHERE date_generation < datetime('now', '-1 year')
    """)
    lignes = c.fetchall()

    if not lignes:
        conn.close()
        return "Aucun proforma validé à archiver."

    # Création du dossier archives
    os.makedirs("archives", exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"archives/proformas_payes_{date_str}.csv"
    zip_filename = f"archives/proformas_payes_{date_str}.zip"

    # Export CSV
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([col for col in lignes[0].keys()])
        for row in lignes:
            writer.writerow([row[col] for col in row.keys()])

    # Compression ZIP
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_filename)

    # Suppression des lignes archivées
    c.execute("""
        DELETE FROM proformas_payes
        WHERE date_generation < datetime('now', '-1 year')
    """)
    conn.commit()
    conn.close()

    return send_file(zip_filename, as_attachment=True)
