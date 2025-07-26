from flask import Flask, request, jsonify, session

from database import get_connection, get_user
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'supersecret'

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = get_user(data["username"])
    if user and user[2] == data["password"]:
        session["user_id"] = user[0]
        session["is_admin"] = bool(user[3])
        return jsonify({"success": True, "is_admin": bool(user[3])})
    return jsonify({"success": False}), 401

@app.route("/availability", methods=["POST"])
def submit_availability():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO availability (user_id, day, start_time, end_time) VALUES (?, ?, ?, ?)",
                (session["user_id"], data["day"], data["start"], data["end"]))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/assignments")
def get_assignments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT day, start_time, end_time, username FROM shifts JOIN users ON shifts.user_id = users.id")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
