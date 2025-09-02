from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="ufouma",  # change this
        host="localhost",
        port="5432"
    )
    return conn


# ---------- CREATE TABLE ----------
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clubs (
            id SERIAL PRIMARY KEY,
            club_name VARCHAR(255) NOT NULL,
            club_base VARCHAR(255) NOT NULL,
            club_type VARCHAR(100) NOT NULL,
            club_director VARCHAR(255) NOT NULL,
            club_category VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()


# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        club_name = request.form["clubName"]
        club_base = request.form["clubBase"]
        club_type = request.form["clubType"]
        club_director = request.form["clubDirector"]
        club_category = request.form["clubCategory"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO clubs (club_name, club_base, club_type, club_director, club_category)
            VALUES (%s, %s, %s, %s, %s)
        """, (club_name, club_base, club_type, club_director, club_category))
        conn.commit()
        cur.close()
        conn.close()

        return redirect("/")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT club_name, club_base, club_type, club_director, club_category FROM clubs ORDER BY id DESC")
    clubs = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", clubs=clubs)
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/clubs")
def clubs():
    return render_template("clubs.html")

if __name__ == "__main__":
    app.run(debug=True)
