from flask import Blueprint, render_template, session, redirect, url_for
from db import get_db_connection

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.index"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(email) FROM first")
    total_clients = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM first WHERE first_mail_date IS NOT NULL")
    initial_mail_sent = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM first WHERE status = 'replied'")
    received_mail = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        user=session["user"],
        total_clients=total_clients,
        initial_mail_sent=initial_mail_sent,
        received_mail=received_mail
    )
