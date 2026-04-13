from flask import Flask, request
import sqlite3
import subprocess
import os

app = Flask(__name__)

# Vulnérabilité : mot de passe en dur dans le code
DB_PASSWORD = "admin123"
SECRET_KEY = "hardcoded_secret_key_123"

def get_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    conn.commit()
    return conn

@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    conn = get_db()
    # Vulnérabilité : injection SQL
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query).fetchall()
    return str(result)

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # Vulnérabilité : injection de commande
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output

@app.route("/file")
def read_file():
    filename = request.args.get("name", "")
    # Vulnérabilité : path traversal
    with open(os.path.join("/tmp", filename)) as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)
