from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Environment variables (important for Docker later)
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "notesdb")


def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT NOT NULL
            )
            """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                source INT,
                target INT
            )
            """)

    conn.commit()

    if request.method == "POST":
        note = request.form["note"]
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
        conn.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    
   
    cursor.close()
    conn.close()

    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)