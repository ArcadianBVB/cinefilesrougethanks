import sqlite3
import csv
import os
from datetime import datetime
import zipfile

# Configuration
DB = "stock.db"
ARCHIVE_DIR = "archives"
ZIP_THRESHOLD_KB = 100  # Seuil pour zip

# Préparation
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")

if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

# Connexion base de données
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# 1. Vérifier ou créer la table proformas
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='proformas';")
if not c.fetchone():
    c.execute("""
        CREATE TABLE proformas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande TEXT,
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
            statut TEXT
        );
    """)

# 2. Vérifier ou créer la table des proformas payés
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='proformas_payes';")
if not c.fetchone():
    c.execute("""
        CREATE TABLE proformas_payes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_commande TEXT,
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
            statut TEXT
        );
    """)

# 3. Mise à jour des statuts
# 3.1 → Expirer après 2 jours
c.execute("""
    UPDATE proformas
    SET statut = 'Expiré'
    WHERE statut NOT IN ('Payé', 'Invalide')
    AND date(date_generation) <= date('now', '-2 days');
""")

# 3.2 → Invalider après 7 jours
c.execute("""
    UPDATE proformas
    SET statut = 'Invalide'
    WHERE statut != 'Payé'
    AND date(date_generation) <= date('now', '-7 days');
""")

# 4. Transfert des payés de +30 jours dans proformas_payes
c.execute("""
    INSERT INTO proformas_payes (
        id_commande, nom_client, contact, type_client, produits,
        montant_total, mode_livraison, frais_livraison, observations,
        date_commande, date_generation, date_expiration, statut
    )
    SELECT
        id_commande, nom_client, contact, type_client, produits,
        montant_total, mode_livraison, frais_livraison, observations,
        date_commande, date_generation, date_expiration, statut
    FROM proformas
    WHERE statut = 'Payé' AND date(date_generation) <= date('now', '-30 days');
""")

# Suppression des payés transférés
c.execute("""
    DELETE FROM proformas
    WHERE statut = 'Payé' AND date(date_generation) <= date('now', '-30 days');
""")

# 5. Export des invalides de +30 jours en CSV
c.execute("""
    SELECT * FROM proformas
    WHERE statut = 'Invalide' AND date(date_generation) <= date('now', '-30 days');
""")
invalides = c.fetchall()

csv_filename = f"{ARCHIVE_DIR}/invalides_{today_str}.csv"
zip_filename = f"{ARCHIVE_DIR}/invalides_{today_str}.zip"

if invalides:
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(invalides[0].keys())
        for row in invalides:
            writer.writerow(row)

    # Compression si le fichier dépasse 100 Ko
    file_size_kb = os.path.getsize(csv_filename) / 1024
    if file_size_kb >= ZIP_THRESHOLD_KB:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_filename, os.path.basename(csv_filename))
        os.remove(csv_filename)

    # Suppression définitive des invalides archivés
    ids_to_delete = [str(row["id"]) for row in invalides]
    c.execute(f"DELETE FROM proformas WHERE id IN ({','.join(ids_to_delete)});")

# Finalisation
conn.commit()
conn.close()
print("Nettoyage automatique terminé avec succès.")
