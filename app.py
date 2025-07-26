from flask import Flask, render_template, request, redirect, session, url_for
from models import init_db, get_user, add_user, is_admin, add_availability, get_all_users, get_schedule, add_shift, get_all_shifts
from scheduler import generate_schedule

import os

app = Flask(__name__)
app.secret_key = 'secret-key'
init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user(request.form['username'], request.form['password'])
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['admin'] = user['admin']
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], admin=session['admin'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin'):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        if request.form['type'] == 'add_user':
            add_user(request.form['username'], request.form['password'], request.form.get('admin') == 'on')
        elif request.form['type'] == 'add_availability':
            add_availability(int(request.form['user_id']), request.form['day'], request.form['start'], request.form['end'])
        elif request.form['type'] == 'generate':
            generate_schedule()
    users = get_all_users()
    schedule = get_schedule()
    return render_template('admin.html', users=users, schedule=schedule)

@app.route('/shifts')
def shifts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    schedule = get_schedule()
    return render_template('shifts.html', schedule=schedule, username=session['username'])


@app.route('/availability', methods=['GET', 'POST'])
def availability():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        from models import add_availability
        add_availability(session['user_id'], request.form['day'], request.form['start'], request.form['end'])
        return redirect(url_for('dashboard'))
    return render_template('availability.html')

@app.route('/admin/shifts', methods=['GET', 'POST'])
def admin_shifts():
    if not session.get('admin'):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        day = request.form['day']
        start = request.form['start']
        end = request.form['end']
        add_shift(day, start, end)
    shifts = get_all_shifts()
    return render_template('admin_shifts.html', shifts=shifts)


if __name__ == '__main__':
    app.run(debug=True)
