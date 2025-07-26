from models import connect

def generate_schedule():
    conn = connect()
    c = conn.cursor()
    c.execute('DELETE FROM schedule')  # Clear old schedule

    # Assign based on least shifts
    c.execute('SELECT user_id, day, start, end FROM availability')
    all = c.fetchall()

    counts = {}
    for user_id, day, start, end in all:
        counts[user_id] = counts.get(user_id, 0)

    all.sort(key=lambda x: counts[x[0]])  # Sort by user load
    for user_id, day, start, end in all:
        if counts[user_id] < 5:  # Max 5 shifts/week
            c.execute('INSERT INTO schedule (user_id, day, start, end) VALUES (?, ?, ?, ?)', (user_id, day, start, end))
            counts[user_id] += 1

    conn.commit()
