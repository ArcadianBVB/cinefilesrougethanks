from flask import Flask
from routes.stock_routes import stock_bp
from routes.commandes_routes import commandes_bp
from apscheduler.schedulers.background import BackgroundScheduler
from routes.exporter_proformas_routes import exporter_bp
import json
import subprocess

app = Flask(__name__)
app.jinja_env.filters['loads'] = json.loads

app.register_blueprint(stock_bp, url_prefix="/stock")
app.register_blueprint(commandes_bp, url_prefix="/commandes")
app.register_blueprint(exporter_bp)

def auto_clean_job():
    subprocess.run(["python", "nettoyage_proformas.py"])

# Planificateur : tous les dimanches à minuit
scheduler = BackgroundScheduler()
scheduler.add_job(auto_clean_job, 'cron', day_of_week='sun', hour=0, minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
