from os import curdir
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# INTEGER is used to be able to increment the id
create_tables = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_tables)

create_tables = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_tables)

cursor.execute("INSERT INTO items VALUES ('item1', 10.99)")

connection.commit()
connection.close()