import sqlite3

conn = sqlite3.connect('employee_scheduler.sqlite')
c = conn.cursor()

# Add an admin user (change username and password as you like)
c.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", ('admin', 'adminpass', 1))

# Add a regular user
c.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", ('employee1', 'password123', 0))

conn.commit()
conn.close()

print("Users added!")
