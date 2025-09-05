from flask import Flask, session, redirect, url_for
import os
from db import get_db_connection

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.client_routes import client_bp
from routes.email_routes import email_bp
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ------------------ Uploads ------------------
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ------------------ Register Blueprints ------------------
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
app.register_blueprint(email_bp)
app.register_blueprint(dashboard_bp)

# ------------------ Root Redirect ------------------
@app.route("/")
def root_redirect():
    if "user" in session:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.index"))

# ------------------ Run ------------------
if __name__ == "__main__":
    app.run(debug=True)
