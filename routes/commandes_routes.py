from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import random
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
