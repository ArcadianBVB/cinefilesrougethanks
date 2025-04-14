from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import random
import string
import json  # Pour charger les produits
from base_price import calculer_prix

# Déclaration du blueprint
commandes_bp = Blueprint('commandes', __name__)

DB_NAME = "stock.db"

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

@commandes_bp.route("/liste")
def liste_commandes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT
            id,
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
        FROM proformas
        ORDER BY id DESC
    ''')
    commandes = c.fetchall()
    conn.close()
    return render_template("commandes_liste.html", commandes=commandes)

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
def delete_commande(proforma_id):
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

@commandes_bp.route("/rechercher")
def rechercher_commandes():
    nom_client = request.args.get("nom_client", "").strip()
    id_commande = request.args.get("id_commande", "").strip()
    statut = request.args.get("statut", "").strip()
    date_debut = request.args.get("date_debut", "")
    date_fin = request.args.get("date_fin", "")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT * FROM proformas WHERE 1=1"
    params = []

    if nom_client:
        query += " AND nom_client LIKE ?"
        params.append(f"%{nom_client}%")

    if id_commande:
        query += " AND id_commande LIKE ?"
        params.append(f"%{id_commande}%")

    if statut:
        query += " AND statut = ?"
        params.append(statut)

    if date_debut:
        query += " AND date_expiration >= ?"
        params.append(date_debut)

    if date_fin:
        query += " AND date_expiration <= ?"
        params.append(date_fin)

    c.execute(query, params)
    commandes = c.fetchall()
    conn.close()

    return render_template("commandes_liste.html", commandes=commandes)
