from flask import Flask
from routes.stock_routes import stock_bp, init_db
from routes.commandes_routes import commandes_bp, init_proformas_db

app = Flask(__name__)

# Enregistrement des Blueprints
app.register_blueprint(stock_bp)
app.register_blueprint(commandes_bp)

if __name__ == "__main__":
    # Initialisation de la base pour le module Stock
    init_db()
    # Initialisation de la table proformas pour le module Commandes & Proformas
    init_proformas_db()
    app.run(debug=True)
