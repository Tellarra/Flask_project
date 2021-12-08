import sqlite3

connection = sqlite3.connect('data.db')

# The cursors is like the one in our computer
# We can point it out where we want to do our query
# The cursor run a query and store the result
cursor = connection.cursor()

# This is a schema
create_table = "CREATE TABLE users (id int, username text, password text )"
# Run Query
cursor.execute(create_table)

user = (1, "Marie", "test")
# SQL Query
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# Run query
cursor.execute(insert_query, user)

users = [
    (2, "Pata", "gfh"),
    (3, "Quentin", "qwe")
]

cursor.executemany(insert_query, users)

# We want to retrieve information
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query) :
    print(row)


# We need to save all of our changes
connection.commit()

# As a good practice it is better to close it
# So it doesn't consumme too much resources
connection.close()