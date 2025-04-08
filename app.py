from flask import Flask
from routes.stock_routes import stock_bp
from routes.commandes_routes import commandes_bp

app = Flask(__name__)

# Enregistrement des blueprints avec leurs préfixes respectifs
app.register_blueprint(stock_bp, url_prefix="/stock")
app.register_blueprint(commandes_bp, url_prefix="/commandes")

if __name__ == "__main__":
    app.run(debug=True)
