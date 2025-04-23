import sqlite3

conn = sqlite3.connect("stock.db")
c = conn.cursor()

exemples = [
    ("Masaya", "+243897...", "National", '[{"titre": "Titanic", "quantite": 1, "prix": 2.0, "total": 2.0}]',
     2.0, "Téléchargement", 0.0, "Test ancien 1", "2023-03-15 12:00:00", "2023-03-15 12:00:00", "2023-03-17 12:00:00", "Payé", "ID20230315A001"),

    ("Gédéon", "+243812...", "International", '[{"titre": "Shrek", "quantite": 1, "prix": 3.0, "total": 3.0}]',
     3.0, "WhatsApp", 0.0, "Test ancien 2", "2023-08-01 10:35:00", "2023-08-01 10:35:00", "2023-08-03 10:35:00", "Payé", "ID20230801B002"),
]

for e in exemples:
    c.execute("""
        INSERT INTO proformas_payes (
            nom_client, contact, type_client, produits, montant_total, 
            mode_livraison, frais_livraison, observations, date_commande, 
            date_generation, date_expiration, statut, id_commande
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, e)

conn.commit()
conn.close()

print("Proformas anciens insérés sans erreur.")
