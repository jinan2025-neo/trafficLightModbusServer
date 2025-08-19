#!/usr/bin/env python3
"""
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
from modbus_func import read_signals, write_flag

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
    return modbus_func.read_signals(client)
    # --- END STUB ---


def write_flag_coil(client, value: bool) -> bool:
    """Write a single flag coil.

    Returns True on success, False otherwise.

    """
    # --- BEGIN STUB ---
    # Simulate success
    return write_flag(client, value)
    # --- END STUB ---


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.route("/")
@login_required
def index():
    return render_template_string(
        DASHBOARD_HTML,
        username=current_user.username,
        poll_ms=POLL_MS,
    )


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
    return render_template_string(LOGIN_HTML, error=error)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Modbus server settings
MODBUS_SERVER_IP = '10.3.21.91'
MODBUS_SERVER_PORT = 502
UNIT_ID = 1

# Global variable to store the latest Modbus data
modbus_data = {}

# Function to maintain a persistent connection and read data every 500 ms
def modbus_worker():
    global modbus_data
    global global_client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT)  # Replace with your Modbus server IP and port
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

@app.route("/write_flag", methods=["POST"]) 
@login_required
def write_flag():
    try:
        raw = request.form.get("flag") or request.json.get("flag") if request.is_json else None
        val = str(raw).lower() in {"1", "true", "on", "yes"}
        ok = write_flag_coil(global_client,val)
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
# Templates (Jinja2 inline)
# ----------------------------------------------------------------------------
LOGIN_HTML = r"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login · Modbus Traffic Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { background: #0f172a; color: #e2e8f0; }
      .card { border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,.25); }
      .brand { font-weight: 700; letter-spacing: .5px; }
    </style>
  </head>
  <body class="d-flex align-items-center" style="min-height:100vh;">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card p-4 bg-dark border-0">
            <div class="card-body">
              <h1 class="brand h3 mb-3 text-center">Modbus Traffic Dashboard</h1>
              {% if error %}
              <div class="alert alert-danger" role="alert">{{ error }}</div>
              {% endif %}
              <form method="post" class="vstack gap-3">
                <div>
                  <label class="form-label">Username</label>
                  <input name="username" class="form-control" placeholder="admin" required>
                </div>
                <div>
                  <label class="form-label">Password</label>
                  <input name="password" type="password" class="form-control" placeholder="••••••••" required>
                </div>
                <button class="btn btn-primary w-100" type="submit">Sign in</button>
                <p class="text-secondary small mt-2 text-center">Default: admin / admin</p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""

DASHBOARD_HTML = r"""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard · Modbus Traffic</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { background: #0b1220; color: #e2e8f0; }
      .navy { background: #0f172a; }
      .card { border-radius: 1rem; }
      .lamp { width: 22px; height: 22px; border-radius: 50%; display: inline-block; margin-right: .4rem; border: 2px solid rgba(255,255,255,.15); }
      .lamp.red.on { background: #ef4444; box-shadow: 0 0 12px #ef4444; }
      .lamp.amber.on { background: #f59e0b; box-shadow: 0 0 12px #f59e0b; }
      .lamp.green.on { background: #22c55e; box-shadow: 0 0 12px #22c55e; }
      .lamp.off { background: #1f2937; }
      .muted { color: #94a3b8; }
      .dot { width: 8px; height: 8px; border-radius: 50%; display:inline-block; margin-right: .35rem; }
      .dot.ok { background:#22c55e; }
      .dot.err { background:#ef4444; }
      .footer { color:#94a3b8; }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark navy mb-4">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">🚦 Modbus Traffic</a>
        <div class="d-flex align-items-center ms-auto gap-3">
          <span class="navbar-text">Signed in as <strong>{{ username }}</strong></span>
          <a class="btn btn-outline-light btn-sm" href="{{ url_for('logout') }}">Logout</a>
        </div>
      </div>
      <div class="text-center mt-4">
  <a href="/add_user" class="btn btn-primary">Add New User</a>
</div>
    </nav>

    <div class="container">
      <div class="row g-4" id="cards"></div>

      <div class="card bg-dark border-0 mt-4">
        <div class="card-body">
          <h5 class="card-title text-white">Flag Coil</h5>
          <p class="muted">Change to rush mode (can be extented to more e.g., maintenance mode, emergency stop, etc.).</p>
          <form id="flag-form" class="d-flex align-items-center gap-2">
            <select class="form-select w-auto" id="flag-value">
              <option value="true">ON (True)</option>
              <option value="false">OFF (False)</option>
            </select>
            <button type="submit" class="btn btn-primary">Write Coil</button>
            <span id="flag-status" class="ms-2 muted"></span>
          </form>
        </div>
      </div>

      <p class="footer small mt-4"><span class="dot" id="hb"></span><span id="hb-text">Connecting…</span></p>
    </div>

    <script>
      const pollMs = {{ poll_ms|int }};

      async function fetchTraffic() {
      try {
        const res = await fetch("/api/traffic", { cache: 'no-store' });
        const json = await res.json();
        if (!json.registers) throw new Error('No data received');
        renderCards(json.registers); // Update UI with the Modbus data
        setHeartbeat(true, 'Online');
      } catch (err) {
        console.error(err);
        setHeartbeat(false, 'Error: ' + (err.message || 'offline'));
      }
    }

      function renderCards(items) {
        const host = document.getElementById('cards');
        host.innerHTML = '';
        (items || []).forEach((x, idx) => {
          const red = x.coils?.red ? 'on' : 'off';
          const amber = x.coils?.amber ? 'on' : 'off';
          const green = x.coils?.green ? 'on' : 'off';
          const card = document.createElement('div');
          card.className = 'col-12 col-md-6 col-lg-4';
          card.innerHTML = `
            <div class="card bg-dark border-0 h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h5 class="card-title mb-1 text-white">${x.direction ?? 'Intersection ' + (idx+1)}</h5>
                    <div class="muted small">Addr: ${x.address ?? '—'}</div>
                  </div>
                </div>
                <div class="mt-3 d-flex align-items-center gap-3">
                  <span class="lamp red ${red}"></span> <span class="muted">Red</span>
                  <span class="lamp amber ${amber}"></span> <span class="muted">Amber</span>
                  <span class="lamp green ${green}"></span> <span class="muted">Green</span>
                </div>
              </div>
            </div>`;
          host.appendChild(card);
        });
      }

      function setHeartbeat(ok, text) {
        const dot = document.getElementById('hb');
        const txt = document.getElementById('hb-text');
        dot.className = 'dot ' + (ok ? 'ok' : 'err');
        txt.textContent = text;
      }

      // pull data every 300 ms
      setInterval(fetchTraffic, 300);

      // Flag coil write
      document.getElementById('flag-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const value = document.getElementById('flag-value').value;
        const el = document.getElementById('flag-status');
        el.textContent = 'Writing…';
        try {
          const res = await fetch("{{ url_for('write_flag') }}", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ flag: value })
          });
          const json = await res.json();
          if (!json.ok) throw new Error(json.error || 'Write failed');
          el.textContent = 'Success → ' + json.value;
        } catch (err) {
          el.textContent = 'Error: ' + (err.message || 'Unknown');
        }
      });
    </script>
  </body>
</html>
"""

# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
