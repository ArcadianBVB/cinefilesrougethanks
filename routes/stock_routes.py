from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
from base_price import calculer_prix
def get_pagination_links(page, total_pages, delta=2):
    """
    Retourne une liste de pages et/ou '...' pour un affichage propre.
    Ex : [1, 2, 3, 4, 5, '...', 30] si total_pages=30, page=3, delta=2.
    """
    links = []
    for p in range(1, total_pages + 1):
        if p == 1 or p == total_pages or (p >= page - delta and p <= page + delta):
            links.append(p)
        elif links[-1] != "...":
            links.append("...")
    return links

stock_bp = Blueprint('stock', __name__)
DB_NAME = "stock.db"

@stock_bp.route("/")
def index():
    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    per_page = 15
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM stock")
    total = c.fetchone()[0]

    total_pages = (total + per_page - 1) // per_page

    # Chargement des produits avec pagination
    c.execute("""
        SELECT * FROM stock
        ORDER BY id ASC
        LIMIT ? OFFSET ?
    """, (per_page, offset))
    rows = c.fetchall()
    conn.close()

    # Générer la pagination dynamique
    pagination_links = get_pagination_links(page, total_pages, delta=2)

    return render_template(
        "index.html",
        rows=rows,
        page=page,
        total_pages=total_pages,
        pagination_links=pagination_links,
        per_page=per_page
    )

@stock_bp.route("/rechercher", methods=["GET"])
def rechercher():
    mot_cle = request.args.get("q", "").lower()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM stock WHERE LOWER(titre) LIKE ?", ('%' + mot_cle + '%',))
    resultats = c.fetchall()
    conn.close()
    return render_template(
    "index.html",
    rows=resultats,
    recherche=mot_cle,
    page=1,
    total_pages=1
)

@stock_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form
        titre = data.get("titre")
        type_ = data.get("type")
        qualite = data.get("qualite")
        format_ = data.get("format")
        categorie = data.get("categorie")
        rarete = data.get("rarete")
        acteur = data.get("acteur")
        production = data.get("production")
        saison = data.get("saison")
        episodes = data.get("episodes")
        annee = data.get("annee")
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prix = calculer_prix(type_, qualite, format_, rarete, saison, episodes)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            INSERT INTO stock (
                titre, type, qualite, format, categorie, rarete, prix,
                acteur, production, saison, episodes, annee,
                date_ajout, date_modif
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titre, type_, qualite, format_, categorie, rarete, prix,
              acteur, production, saison, episodes, annee, date_now, date_now))
        conn.commit()
        conn.close()
        return redirect(url_for("stock.index"))
    return render_template("add.html")

@stock_bp.route("/delete/<int:item_id>")
def delete(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM stock WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("stock.index"))

@stock_bp.route("/modifier/<int:item_id>", methods=["GET", "POST"])
def modifier(item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if request.method == "POST":
        data = request.form
        titre = data.get("titre")
        type_ = data.get("type")
        qualite = data.get("qualite")
        format_ = data.get("format")
        categorie = data.get("categorie")
        rarete = data.get("rarete")
        acteur = data.get("acteur")
        production = data.get("production")
        saison = data.get("saison")
        episodes = data.get("episodes")
        annee = data.get("annee")
        date_modif = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prix = calculer_prix(type_, qualite, format_, rarete, saison, episodes)
        c.execute("""
            UPDATE stock SET
                titre=?, type=?, qualite=?, format=?, categorie=?, rarete=?, prix=?,
                acteur=?, production=?, saison=?, episodes=?, annee=?, date_modif=?
            WHERE id=?
        """, (titre, type_, qualite, format_, categorie, rarete, prix,
              acteur, production, saison, episodes, annee, date_modif, item_id))
        conn.commit()
        conn.close()
        return redirect(url_for("stock.index"))
    else:
        c.execute("SELECT * FROM stock WHERE id=?", (item_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return "Enregistrement introuvable", 404
        return render_template("edit.html", item=row)

@stock_bp.route("/prix_auto", methods=["POST"])
def prix_auto():
    data = request.get_json()
    type_ = data.get("type", "")
    format_ = data.get("format", "")
    qualite = data.get("qualite", "")
    rarete = data.get("rarete", "")
    saison = data.get("saison", "")
    episodes = data.get("episodes", "")
    prix = calculer_prix(type_, qualite, format_, rarete, saison, episodes)
    return jsonify({"prix": prix})

