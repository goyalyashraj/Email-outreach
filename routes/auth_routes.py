from flask import Blueprint, render_template, request, redirect, url_for, session
from flask import flash

auth_bp = Blueprint("auth", __name__)
USER_CREDENTIALS = {"admin": "password123"}

@auth_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard.dashboard"))
        else:
            return render_template("index.html", error="Invalid credentials")
    return render_template("index.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.index"))
