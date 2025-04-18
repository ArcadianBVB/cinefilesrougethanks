DROP TABLE IF EXISTS proformas;

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

INSERT INTO proformas (
    id_commande, nom_client, contact, type_client, produits, montant_total,
    mode_livraison, frais_livraison, observations, date_commande,
    date_generation, date_expiration, statut
) VALUES
('ID20250401ABC1', 'Jean Mado', '+243810123456', 'National',
 '[{"titre":"Sam Le Pompier","qualite":"HD","prix":4,"quantite":2,"total":8}]',
 8.0, 'WhatsApp', 0.5, 'Livrer avant 10h', '2025-04-01 09:00:00',
 '2025-04-01 09:00:00', '2025-04-03 09:00:00', 'En attente'),

('ID20250401XYZ9', 'Giselle Tutu', '+243810987654', 'International',
 '[{"titre":"Naruto","qualite":"Full HD","prix":6,"quantite":5,"total":30}]',
 30.0, 'Email', 0, 'Client récurrent', '2025-04-02 10:30:00',
 '2025-04-02 10:30:00', '2025-04-04 10:30:00', 'Payé'),

('ID20250402AAA7', 'Daniel Okito', '+243899123456', 'National',
 '[{"titre":"Breaking Bad","qualite":"HD","prix":8,"quantite":1,"total":8}]',
 8.0, 'Electro', 1.0, 'Livraison express', '2025-04-02 15:45:00',
 '2025-04-02 15:45:00', '2025-04-04 15:45:00', 'Payé'),

('ID20250402SOM3', 'Jeancy Luta', '+243895321000', 'National',
 '[{"titre":"Dora l''exploratrice","qualite":"HD","prix":5,"quantite":3,"total":15}]',
 15.0, 'WhatsApp', 0, '', '2025-04-02 18:00:00',
 '2025-04-02 18:00:00', '2025-04-04 18:00:00', 'Expiré'),

('ID20250403FAN9', 'Sarah Mbayo', '+243812224455', 'International',
 '[{"titre":"Le Roi Lion","qualite":"4K","prix":10,"quantite":1,"total":10}]',
 10.0, 'Email', 0.5, 'Urgent', '2025-04-03 12:15:00',
 '2025-04-03 12:15:00', '2025-04-05 12:15:00', 'Payé');
