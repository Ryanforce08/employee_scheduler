import sqlite3

def connect():
    return sqlite3.connect('employee_scheduler.sqlite', check_same_thread=False)

def init_db():
    conn = connect()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT, password TEXT, admin INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS shifts (
        id INTEGER PRIMARY KEY, day TEXT, start TEXT, end TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY, user_id INTEGER, shift_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(shift_id) REFERENCES shifts(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY, user_id INTEGER, shift_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(shift_id) REFERENCES shifts(id))''')
    conn.commit()

def get_user(username, password):
    c = connect().cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    row = c.fetchone()
    if row:
        return {'id': row[0], 'username': row[1], 'admin': bool(row[3])}
    return None

def is_admin(user_id):
    c = connect().cursor()
    c.execute('SELECT admin FROM users WHERE id=?', (user_id,))
    return bool(c.fetchone()[0])

def add_user(username, password, admin=False):
    c = connect().cursor()
    c.execute('INSERT INTO users (username, password, admin) VALUES (?, ?, ?)', (username, password, int(admin)))
    connect().commit()

def add_availability(user_id, day, start, end):
    conn = connect()
    with conn:
        conn.execute('INSERT INTO availability (user_id, day, start, end) VALUES (?, ?, ?, ?)', (user_id, day, start, end))

def get_all_users():
    c = connect().cursor()
    c.execute('SELECT * FROM users')
    return c.fetchall()

def get_schedule():
    c = connect().cursor()
    c.execute('SELECT u.username, s.day, s.start, s.end FROM schedule s JOIN users u ON s.user_id = u.id')
    return c.fetchall()

def add_shift(day, start, end):
    conn = connect()
    with conn:
        conn.execute('INSERT INTO shifts (day, start, end) VALUES (?, ?, ?)', (day, start, end))

def get_all_shifts():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT id, day, start, end FROM shifts ORDER BY day, start')
    return c.fetchall()
