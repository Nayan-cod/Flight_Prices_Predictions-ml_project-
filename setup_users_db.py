import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Add a sample user
cursor.execute('''
INSERT INTO users (username, password)
VALUES (?, ?)
''', ('admin', generate_password_hash('admin123')))

conn.commit()
conn.close()
