"""
URL Shortener
-------------
A simple Python project that converts long URLs into short, unique
codes and redirects users back to the original URL when visited.

How it works:
- Flask provides the web interface and routes.
- SQLite stores the mapping between short codes and original URLs.
- A random 6-character code is generated for each new URL.

Run:
    pip install flask
    python url_shortener.py

Then open http://127.0.0.1:5000 in your browser.
"""

import sqlite3
import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB_NAME = "urls.db"


# ---------- Database setup ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Helper functions ----------
def generate_short_code(length=6):
    """Generate a random alphanumeric code and ensure it's unique."""
    characters = string.ascii_letters + string.digits
    conn = get_db_connection()
    while True:
        code = "".join(random.choices(characters, k=length))
        existing = conn.execute(
            "SELECT 1 FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if not existing:
            conn.close()
            return code


# ---------- HTML template ----------
HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>URL Shortener</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 60px auto; }
        input[type=text] { width: 70%; padding: 8px; }
        button { padding: 8px 16px; }
        .result { margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px; }
        .history { margin-top: 30px; }
        .history li { margin-bottom: 6px; }
    </style>
</head>
<body>
    <h1>Python URL Shortener</h1>
    <form method="POST" action="/shorten">
        <input type="text" name="original_url" placeholder="Enter a long URL" required>
        <button type="submit">Shorten</button>
    </form>

    {% if short_url %}
    <div class="result">
        <strong>Shortened URL:</strong>
        <a href="{{ short_url }}">{{ short_url }}</a>
    </div>
    {% endif %}

    <div class="history">
        <h3>Recently shortened</h3>
        <ul>
        {% for row in urls %}
            <li>
                <a href="/{{ row['short_code'] }}">{{ request.host_url }}{{ row['short_code'] }}</a>
                &rarr; {{ row['original_url'] }}
            </li>
        {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


# ---------- Routes ----------
@app.route("/")
def home():
    conn = get_db_connection()
    urls = conn.execute(
        "SELECT short_code, original_url FROM urls ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return render_template_string(HOME_PAGE, urls=urls, short_url=None)


@app.route("/shorten", methods=["POST"])
def shorten():
    original_url = request.form["original_url"].strip()

    # Add http:// if missing, so redirects work properly
    if not original_url.startswith(("http://", "https://")):
        original_url = "http://" + original_url

    conn = get_db_connection()

    # If the URL was already shortened before, reuse the same code
    existing = conn.execute(
        "SELECT short_code FROM urls WHERE original_url = ?", (original_url,)
    ).fetchone()

    if existing:
        short_code = existing["short_code"]
    else:
        short_code = generate_short_code()
        conn.execute(
            "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
            (short_code, original_url),
        )
        conn.commit()

    urls = conn.execute(
        "SELECT short_code, original_url FROM urls ORDER BY id DESC LIMIT 10"
    ).fetchall()
    conn.close()

    short_url = request.host_url + short_code
    return render_template_string(HOME_PAGE, urls=urls, short_url=short_url)


@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    conn.close()

    if row:
        return redirect(row["original_url"])
    return "Short URL not found.", 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
