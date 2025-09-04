#!/usr/bin/env python3
"""
The secure version of the simple Modbus TCP traffic light dashboard.
Secure part:
- No SSL/TLS (HTTP only) --> Use HTTPS (flask SSL, SSL/TLS termination in front (e.g., Nginx, Caddy))
- Information leakage via error messages --> Generic error messages, redirect error messages properly on user side
- Possible way to bypass login (not tested) --> Use flask-login properly
- No rate limiting / brute-force protection --> limit the login attempts
others
- use cookie --> use session (safer. recommended in flask)
Flask app: Traffic Light Modbus Dashboard

Features
- Username/password login with flask-login
- Dashboard to monitor remote coil states (stubbed pymodbus calls)
- Endpoint to write a flag coil (stubbed pymodbus call)
- Simple Bootstrap UI with auto-refresh via fetch() polling

Run
-----
$ python app.py

Default credentials: admin / admin

Notes
-----
Replace the TODO sections in `read_traffic_coils()` and `write_flag_coil()`
with your actual pymodbus client logic. Keep the return schema the same
so the UI continues to work.
"""
from __future__ import annotations
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Dict, Any, List

# self-defined function that calls pymodbus to read the traffic light coils from the server
from modbus_func import read_signals, write_flag_coil, on_off_coil

from flask import (
    Flask, render_template_string, request, redirect, url_for,
    flash, jsonify, session, abort, render_template
)
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from pymodbus.client.tcp import ModbusTcpClient
from threading import Thread
import time
# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
POLL_MS = int(os.environ.get("POLL_MS", "500"))  # client refresh interval: 500ms

app = Flask(__name__)
app.config.update(SECRET_KEY=SECRET_KEY)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# ----------------------------------------------------------------------------
# Database helpers (SQLite for users)
# ----------------------------------------------------------------------------

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_db_connection()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL,
                password_hash TEXT NOT NULL
            );
            """
        )
        conn.commit()
        # Create default admin/admin if not present
        cur = conn.execute("SELECT id FROM users WHERE username=?", ("admin",))
        if cur.fetchone() is None:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", generate_password_hash("admin"), 'admin'),
            )
            conn.commit()

# add a new user to users.db (only admin is allowed to do this)
# this is a function triggered by a POST request from the UI
def add_new_user(username: str, password: str) -> None:
    """Add a new user to the database."""
    with closing(get_db_connection()) as conn:
        try:
            password_hash = generate_password_hash(password)
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash,'regular_user'),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Username already exists")
        except Exception as e:
            raise RuntimeError(f"Failed to add user: {str(e)}")

# ----------------------------------------------------------------------------
# User model for flask-login
# ----------------------------------------------------------------------------
class User(UserMixin):
    def __init__(self, user_id: int, username: str, password_hash: str, role: str):
        self.id = str(user_id)
        self.username = username
        self.password_hash = password_hash
        self.role = role  

    @staticmethod
    def get(user_id: str) -> "User | None":
        with closing(get_db_connection()) as conn:
            row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
            if row:
                return User(row["id"], row["username"], row["password_hash"], row["role"]) 
            return None

    @staticmethod
    def get_by_username(username: str) -> "User | None":
        with closing(get_db_connection()) as conn:
            row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
            if row:
                return User(row["id"], row["username"], row["password_hash"], row["role"]) 
            return None


@login_manager.user_loader
def load_user(user_id: str):
    return User.get(user_id)


# ----------------------------------------------------------------------------
# Stubbed pymodbus integration points
# ----------------------------------------------------------------------------
# Replace the bodies of these functions with real pymodbus logic.
# Keep the return structures stable so the UI keeps working.


def read_traffic_coils(client) -> List[Dict[str, Any]]:
    """Return a list of intersections with coil states.

    Expected structure per intersection:
    {
      "direction": "Junction A",
      "address": 1,  # (optional) starting coil address
      "coils": {"red": True, "amber": False, "green": False}
    }

    TODO: Replace with actual pymodbus read_coils() calls based on your mapping.
    """
    # --- BEGIN STUB ---
    return read_signals(client)
    # --- END STUB ---


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.route("/")
@login_required
def index():
    return render_template("dashboard.html", username=current_user.username, poll_ms=POLL_MS)
    # return render_template_string(
    #     DASHBOARD_HTML,
    #     username=current_user.username,
    #     poll_ms=POLL_MS,
    # )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.get_by_username(username)
        if not user or not check_password_hash(user.password_hash, password):
            error = "Invalid username or password"
        else:
            # Store the user's role in the session
            print(f'User {user.username} logged in with role {user.role}')
            session["role"] = user.role
            session["username"] = user.username

            login_user(user)
            return redirect(url_for("index"))
    # return render_template_string(LOGIN_HTML, error=error)
    return render_template("login.html", error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Modbus server settings
MODBUS_SERVER_IP = '10.3.243.70'
# MODBUS_SERVER_IP = '10.3.21.91'
MODBUS_SERVER_PORT = 502
UNIT_ID = 1

# Global variable to store the latest Modbus data
modbus_data = {}

# Function to maintain a persistent connection and read data every 500 ms
def modbus_worker():
    global modbus_data
    global global_client 
    global_client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)  # Replace with your Modbus server IP and port
    if global_client.connect():
        print("Connected to Modbus server")
        while True:
            try:
                # Read data (e.g., holding registers starting at address 0)
                result = read_signals(global_client)  # Adjust address and count as needed
                modbus_data = {"registers": result}
                # print(result)
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.5)  # Wait 500 ms before the next read
    else:
        print("Failed to connect to Modbus server")
    global_client.close()

# Start the Modbus worker in a separate thread
Thread(target=modbus_worker, daemon=True).start()


# API endpoint to serve the latest Modbus data
@app.route('/api/traffic', methods=['GET'])
def get_traffic():
    return jsonify(modbus_data)

# write the on/off coil (coil 801) to the given boolean value
@app.route("/write_on_off", methods=["POST"])
@login_required
def write_on_off():
    try:
        # print('request data:',request.data)
        # print('form data:',request.form)
        # print('json data:',request.json)
        # print('raw:',request.form.get("flag"),request.json.get('flag'), request.is_json)
        raw = request.form.get("state") or request.json.get("state") if request.is_json else None
        val = str(raw).lower() in {"1", "true", "on", "yes"}
        ok = on_off_coil(global_client,val)
        if not ok:
            return jsonify({"ok": False, "error": "Write coil failed"}), 500
        return jsonify({"ok": True, "value": val})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500




@app.route("/write_flag", methods=["POST"]) 
@login_required
def write_flag():
    try:
        if request.is_json:
          raw = request.json.get("flag")
        else:
          raw = request.form.get("flag") or None
        val = str(raw).lower() in {"1", "true", "on", "yes"}
        ok = on_off_coil(global_client,val)
        if not ok:
            return jsonify({"ok": False, "error": "Write coil failed"}), 500
        return jsonify({"ok": True, "value": val})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# Mock function to check if the current user is an admin
def is_admin():
    print(f'Checking if user is admin: {session.get("role")}')
    return session.get("role") == "admin"

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if not is_admin():
        abort(403)  # Return 403 Forbidden if the user is not an admin

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            add_new_user(username, password)  # Call the function from your code
            return redirect(url_for("success_page"))  # Redirect to a success page
        except ValueError as ve:
            return render_template("add_user.html", error=str(ve))
        except RuntimeError as re:
            return render_template("add_user.html", error=str(re))

    # Render the form for GET requests
    return render_template("add_user.html")

# Example success page route
@app.route("/success")
def success_page():
    # redirect to the dashboard after displaying the success message
    flash("User added successfully!", "success")
    return redirect(url_for("index"))  # Redirect to the dashboard or another page

# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", "5000"))
    # app.run(host="0.0.0.0", port=port, debug=True)
    app.run(host="0.0.0.0", port=port, debug=True, ssl_context=('cert.pem', 'key.pem')) # Configure TLS to serve over HTTPS.