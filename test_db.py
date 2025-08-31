import mysql.connector

# Use the same db_config as in crypto_dashboard.py
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Match your password
    'database': 'crypto_db'
}

try:
    # Attempt to connect
    db = mysql.connector.connect(**db_config)
    print("Connection successful:", db.is_connected())

    # Perform a simple query
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    print("Simple query result:", cursor.fetchone())

    # Insert a test row into portfolio
    query = "INSERT INTO portfolio (coin_id, amount, created_at) VALUES (%s, %s, %s)"
    values = ("test_coin", 1.0, "2025-06-01 12:00:00")
    cursor.execute(query, values)
    db.commit()
    print("Test insert successful, rows affected:", cursor.rowcount)

    # Verify the insert
    cursor.execute("SELECT * FROM portfolio WHERE coin_id = 'test_coin'")
    print("Inserted row:", cursor.fetchone())

    # Close the connection
    db.close()
    print("Connection closed")
except mysql.connector.Error as err:
    print("MySQL error details:", str(err))
except Exception as e:
    print("Unexpected error:", str(e))
