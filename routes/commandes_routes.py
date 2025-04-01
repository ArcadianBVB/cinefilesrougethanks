from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime, timedelta
import os

commandes_bp = Blueprint('commandes', __name__, url_prefix='/commandes')
DB_NAME = "stock.db"  # On utilise la même DB pour simplifier

def init_proformas_db():
    """
    Crée la table 'proformas' si elle n'existe pas encore.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS proformas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_client TEXT,
            contact TEXT,
            type_client TEXT,
            produits TEXT,
            montant_total REAL,
            mode_livraison TEXT,
            frais_livraison REAL,
            observations TEXT,
            date_commande TEXT,
            date_generation TEXT,
            date_expiration TEXT,
            statut TEXT,
            chemin_fichier TEXT
        )
    ''')
    conn.commit()
    conn.close()

@commandes_bp.route("/nouvelle", methods=["GET", "POST"])
def nouvelle_commande():
    if request.method == "POST":
        # Récupération des données du formulaire
        nom_client = request.form.get("nom_client")
        contact = request.form.get("contact")
        type_client = request.form.get("type_client")
        produits = request.form.get("produits")  # Liste des produits, formaté en chaîne
        montant_total = request.form.get("montant_total")
        mode_livraison = request.form.get("mode_livraison")
        frais_livraison = request.form.get("frais_livraison")
        observations = request.form.get("observations")
        date_commande = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_generation = date_commande
        # Calcul de la date d'expiration (48h après la génération)
        date_expiration = (datetime.now() + timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
        statut = "En attente"
        
        # Insertion dans la table proformas
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO proformas (
                nom_client, contact, type_client, produits, montant_total,
                mode_livraison, frais_livraison, observations, date_commande,
                date_generation, date_expiration, statut, chemin_fichier
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nom_client, contact, type_client, produits, montant_total,
            mode_livraison, frais_livraison, observations, date_commande,
            date_generation, date_expiration, statut, ""  # Le chemin vers le PDF sera mis à jour après génération
        ))
        conn.commit()
        conn.close()
        
        # Ici, on pourra ajouter l'appel à la fonction de génération du PDF, par exemple
        # generate_proforma_pdf(nom_client, date_generation, ...)
        
        return redirect(url_for("commandes.liste_commandes"))
    return render_template("nouvelle_commande.html")

@commandes_bp.route("/liste")
def liste_commandes():
    # Récupération de toutes les commandes/proformas
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM proformas ORDER BY id DESC")
    commandes = c.fetchall()
    conn.close()
    return render_template("commandes_liste.html", commandes=commandes)

@commandes_bp.route("/view/<int:proforma_id>")
def view_proforma(proforma_id):
    # Affichage de l'aperçu du PDF dans le navigateur (optionnel)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM proformas WHERE id=?", (proforma_id,))
    proforma = c.fetchone()
    conn.close()
    if not proforma:
        return "Proforma introuvable", 404
    return render_template("proforma_view.html", proforma=proforma)

@commandes_bp.route("/changer_statut/<int:proforma_id>/<nouveau_statut>")
def changer_statut(proforma_id, nouveau_statut):
    # Permet de modifier le statut manuellement (En attente, Payé, Livré, Expiré)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE proformas SET statut=? WHERE id=?", (nouveau_statut, proforma_id))
    conn.commit()
    conn.close()
    return redirect(url_for("commandes.liste_commandes"))
