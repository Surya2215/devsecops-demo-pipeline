"""
Small demo Flask app used to exercise the DevSecOps pipeline.
Deliberately kept tiny — its only job is to give SAST/SCA/secret-scan
something real to run against.
"""

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "demo.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/users/<int:user_id>")
def get_user(user_id):
    """
    SAFE pattern: parameterized query, not string concatenation.
    This is the fixed version of the classic SQLi example —
    kept here on purpose so the pipeline's SAST stage has a clean
    pattern to compare against if you ever want to demo the
    'vulnerable vs fixed' difference for an interview.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "user not found"}), 404

    return jsonify({"id": row[0], "username": row[1]})


@app.route("/echo", methods=["POST"])
def echo():
    """
    SAFE pattern: returns JSON as JSON, no raw HTML string building,
    so there's no reflected-XSS-shaped sink here for SAST to flag.
    """
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data})


# --- Intentional demo finding, clearly labeled ---
# This is a fake, non-functional placeholder credential kept here on
# PURPOSE so the secret-scanning stage of the pipeline has something
# real to catch on the first run. Delete this line once you've taken
# your screenshot for the portfolio/interview — it does not connect
# to anything real.



if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
