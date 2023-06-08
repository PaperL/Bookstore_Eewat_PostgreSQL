import sqlite3

# Connect to the SQLite database file
connection = sqlite3.connect('fe/data/book.db')

# Create a cursor object
cursor = connection.cursor()

# Execute the SQL query to retrieve table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Fetch all the table names
tables = cursor.fetchall()

# Iterate through the tables
for table in tables:
    table_name = table[0]

    # Execute a query to count the number of rows in the table
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")

    # Fetch the result of the query
    result = cursor.fetchone()

    # Print the table name and row count
    print(f"Table: {table_name}")
    print(f"Number of rows: {result[0]}")
    print()

# Close the cursor and the database connection
cursor.close()
connection.close()
