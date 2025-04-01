from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
from base_price import calculer_prix

stock_bp = Blueprint('stock', __name__, url_prefix='/')
DB_NAME = "stock.db"

def init_db():
    """
    Crée la table 'stock' si elle n'existe pas encore.
    Pas de décorateur, car certaines versions de Flask ne supportent pas
    before_app_first_request / before_app_request sur un Blueprint.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT,
            type TEXT,
            qualite TEXT,
            format TEXT,
            categorie TEXT,
            rarete TEXT,
            prix REAL,
            acteur TEXT,
            production TEXT,
            saison TEXT,
            episodes TEXT,
            annee TEXT,
            date_ajout TEXT,
            date_modif TEXT
        )
    ''')
    conn.commit()
    conn.close()

@stock_bp.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM stock ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("index.html", rows=rows)

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

        # Calcul du prix
        prix = calculer_prix(type_, qualite, format_, rarete, saison, episodes)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO stock (
                titre, type, qualite, format, categorie, rarete, prix,
                acteur, production, saison, episodes, annee,
                date_ajout, date_modif
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titre, type_, qualite, format_, categorie, rarete, prix,
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
        c.execute('''
            UPDATE stock
            SET titre=?,
                type=?,
                qualite=?,
                format=?,
                categorie=?,
                rarete=?,
                prix=?,
                acteur=?,
                production=?,
                saison=?,
                episodes=?,
                annee=?,
                date_modif=?
            WHERE id=?
        ''', (titre, type_, qualite, format_, categorie, rarete, prix,
              acteur, production, saison, episodes, annee,
              date_modif, item_id))
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
