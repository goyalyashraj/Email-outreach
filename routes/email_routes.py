from flask import Blueprint, render_template, session, redirect, url_for

email_bp = Blueprint("email", __name__)

@email_bp.route("/email")
def email():
    if "user" not in session:
        return redirect(url_for("auth.index"))
    return render_template("email.html", user=session["user"])
