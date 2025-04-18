-- Insertion de 50 commandes fictives dans la table proformas
BEGIN TRANSACTION;
INSERT INTO proformas (id_commande, nom_client, contact, type_client, produits, montant_total, mode_livraison, frais_livraison, observations, date_commande, date_generation, date_expiration, statut) VALUES
('CMD0001', 'Jean Kasa', '+243810000001', 'National', '[{"titre":"Sam Le Pompier","qualite":"HD","prix":4,"quantite":2,"total":8}]', 8, 'WhatsApp', 0.5, '', '2025-04-01 08:00:00', '2025-04-01 08:00:00', '2025-04-03 08:00:00', 'En attente'),
('CMD0002', 'Sarah Mutombo', '+243810000002', 'International', '[{"titre":"Naruto","qualite":"Full HD","prix":6,"quantite":4,"total":24}]', 24, 'Email', 0, '', '2025-04-01 09:30:00', '2025-04-01 09:30:00', '2025-04-03 09:30:00', 'Payé'),
('CMD0003', 'David Luyindula', '+243810000003', 'National', '[{"titre":"Le Roi Lion","qualite":"4K","prix":10,"quantite":1,"total":10}]', 10, 'Electro', 1, '', '2025-04-01 10:00:00', '2025-04-01 10:00:00', '2025-04-03 10:00:00', 'Payé'),
('CMD0004', 'Aline Bemba', '+243810000004', 'International', '[{"titre":"Dora l''exploratrice","qualite":"HD","prix":5,"quantite":3,"total":15}]', 15, 'WhatsApp', 0, '', '2025-04-01 11:00:00', '2025-04-01 11:00:00', '2025
":8,"quantite":2,"total":16}]', 16, 'Electro', 1, '', '2025-04-01 12:30:00', '2025-04-01 12:30:00', '2025-04-03 12:30:00', 'Payé'),
('CMD0006', 'Marie Tumba', '+243810000006', 'International', '[{"titre":"Naruto","qualite":"Full HD","prix":6,"quantite":3,"total":18}]', 18, 'Email', 0, '', '2025-04-01 13:30:00', '2025-04-01 13:30:00', '2025-04-03 13:30:00', 'Payé'),
('CMD0007', 'Micheline Konga', '+243810000007', 'National', '[{"titre":"Sam Le Pompier","qualite":"HD","prix":4,"quantite":4,"total":16}]', 16, 'WhatsApp', 0.5, '', '2025-04-01 14:00:00', '2025-04-01 14:00:00', '2025-04-03 14:00:00', 'Expiré'),
('CMD0008', 'Oscar Mbuyi', '+243810000008', 'International', '[{"titre":"Breaking Bad","qualite":"HD","prix":8,"quantite":1,"total":8}]', 8, 'Email', 0.5, '', '2025-04-01 15:00:00', '2025-04-01 15:00:00', '2025-04-03 15:00:00', 'En attente'),
('CMD0009', 'Alice Nkulu', '+243810000009', 'National', '[{"titre":"Dora l''exploratrice","qualite":"HD","prix":5,"quantite":2,"total":10}]', 10, 'WhatsApp', 0.5, '', '2025-04-01 16:00:00', '2025-04-01 16:00:00', '2025-04-03 16:00:00', 'Payé'),
('CMD0010', 'Fabrice Kitenge', '+243810000010', 'National', '[{"titre":"Naruto","qualite":"Full HD","prix":6,"quantite":2,"total":12}]', 12, 'Electro', 1, '', '2025-04-01 17:00:00', '2025-04-01 17:00:00', '2025-04-03 17:00:00', 'Expiré'),

-- (poursuivre jusqu'à CMD0050 de la même façon...)
