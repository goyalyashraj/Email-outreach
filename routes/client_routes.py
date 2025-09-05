from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
import os, csv
from db import get_db_connection

client_bp = Blueprint("client", __name__)

# ------------------ Client Management ------------------
@client_bp.route("/client-management", methods=["GET", "POST"])
def client_management():
    if "user" not in session:
        return redirect(url_for("auth.index"))  # 🔑 updated to auth.index

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # fetch results as dict
    cursor.execute("SELECT * FROM first")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("client_management.html", clients=clients)

# ------------------ Add Client ------------------
@client_bp.route("/client/add", methods=["GET", "POST"])
def add_client():
    if "user" not in session:
        return redirect(url_for("auth.index"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        company_name = request.form["company_name"]
        company_url = request.form["company_url"]
        linkedin = request.form["linkedin"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO first (name, email, company_name, company_url, linkedin) VALUES (%s, %s, %s, %s, %s)",
            (name, email, company_name, company_url, linkedin),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("client.client_management"))

    return render_template("add_client.html")

# ------------------ Upload CSV ------------------
@client_bp.route("/upload-csv", methods=["POST"])
def upload_csv():
    if "user" not in session:
        return redirect(url_for("auth.index"))

    if "file" not in request.files:
        flash("No file part", "danger")
        return redirect(url_for("client.client_management"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file", "danger")
        return redirect(url_for("client.client_management"))

    if file and file.filename.endswith(".csv"):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Insert into DB
        conn = get_db_connection()
        cursor = conn.cursor()
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute(
                    "INSERT INTO first (name, email, company_name, company_url, linkedin) VALUES (%s, %s, %s, %s, %s)",
                    (
                        row.get("name"),
                        row.get("email"),
                        row.get("company_name"),
                        row.get("company_url"),
                        row.get("linkedin"),
                    ),
                )
        conn.commit()
        cursor.close()
        conn.close()

        flash("CSV uploaded and data inserted successfully!", "success")
    else:
        flash("Invalid file type. Please upload a .csv file", "danger")

    return redirect(url_for("client.client_management"))

# ------------------ Client Table Partial ------------------
@client_bp.route("/client-table")
def client_table_partial():
    if "user" not in session:
        return redirect(url_for("auth.index"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM first")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("partials/client_table.html", clients=clients)
