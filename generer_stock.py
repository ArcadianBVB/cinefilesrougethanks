import sqlite3
from datetime import datetime
import random

# Nom du fichier DB
db_file = "stock.db"

# Connexion à la base de données (sera créée si elle n'existe pas)
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Création de la table stock si elle n'existe pas déjà
c.execute("""
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
""")

# Pour le test, on vide la table existante
c.execute("DELETE FROM stock")

# Listes pour générer des données aléatoires
types = ["film", "série", "novelas", "dessin animé", "documentaire", "animé 3d"]
qualites = ["HD", "Full HD", "4K", "SD"]
# Formats associés par type (pour simplifier)
formats = {
    "film": "long métrage",
    "série": "épisode",
    "novelas": "épisode",
    "dessin animé": "court métrage",
    "documentaire": "long métrage",
    "animé 3d": "court métrage"
}

# Variables constantes pour la démo
categorie = "Catégorie A"
annee = "2023"
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Boucle d'insertion de 450 éléments
for i in range(1, 451):
    # Choix cyclique d'un type
    t = types[(i - 1) % len(types)]
    # Choix aléatoire d'une qualité
    q = random.choice(qualites)
    # Format basé sur le type, avec une valeur par défaut
    f = formats.get(t, "long métrage")
    # Rareté : "Rare" pour chaque 10ème élément, sinon "Normal"
    r = "Rare" if i % 10 == 0 else "Normal"
    # Prix aléatoire entre 1 et 20 (pour l'exemple)
    p = round(random.uniform(1, 20), 2)
    # Acteur et production fictifs
    acteur = f"Acteur {i}"
    prod = f"Production {i}"
    # Pour les types "série" et "novelas", on renseigne les saisons et épisodes
    if t in ["série", "novelas"]:
        s = "1,2,3"
        e = "5,6,7"
    else:
        s = ""
        e = ""
    
    # Insertion dans la base
    c.execute("""
        INSERT INTO stock (
            titre, type, qualite, format, categorie, rarete, prix, acteur, production, saison, episodes, annee, date_ajout, date_modif
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"Produit {i}", t, q, f, categorie, r, p, acteur, prod, s, e, annee, current_time, current_time
    ))

# Sauvegarder les modifications et fermer la connexion
conn.commit()
conn.close()

print("Base de données 'stock.db' préremplie avec 450 éléments générée avec succès.")
