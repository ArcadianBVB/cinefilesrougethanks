import sqlite3
from datetime import datetime

# Connexion
conn = sqlite3.connect("stock.db")
c = conn.cursor()

# Lire tous les proformas existants
c.execute("SELECT id, date_generation FROM proformas_payes")
proformas = c.fetchall()

for id_, date_gen in proformas:
    if not date_gen:
        continue

    try:
        date_obj = datetime.strptime(date_gen, "%Y-%m-%d %H:%M:%S")
        annee = str(date_obj.year)
        mois = date_obj.strftime("%B")
        jour = str(date_obj.day).zfill(2)
        jour_semaine = date_obj.strftime("%A")

        c.execute("""
            UPDATE proformas_payes
            SET annee = ?, mois = ?, jour = ?, jour_semaine = ?
            WHERE id = ?
        """, (annee, mois, jour, jour_semaine, id_))

    except Exception as e:
        print(f"Erreur sur ID {id_}: {e}")

conn.commit()
conn.close()

print("Colonnes annee, mois, jour, jour_semaine remplies avec succès.")
