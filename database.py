import sqlite3

def get_connection():
    return sqlite3.connect("employee_scheduler.sqlite")

def create_user(username, password, is_admin=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
                (username, password, int(is_admin)))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    return cur.fetchone()
