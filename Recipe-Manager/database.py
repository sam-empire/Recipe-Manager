import sqlite3

# Connect to the database
try:
    connection = sqlite3.connect("recipes.db")
    with open("schema.sql") as f:
        connection.executescript(f.read())
    connection.commit()
finally:
    connection.close()

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn
