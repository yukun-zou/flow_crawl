import sqlite3

# Connect to SQLite
connection = sqlite3.connect('flows.db')
# Create a cursor object
cursor = connection.cursor()

#example S
S = {'debug', 'function', 'mqtt in', 'mqtt out', 'mqtt-broker'}
try:
    # Build query
    query = f"SELECT DISTINCT flows.name FROM flows WHERE"
    for node in S:
        query += f" core_nodes LIKE '%{node}%' AND"
    # Remove the trailing AND
    query = query.rstrip('AND')

    cursor.execute(query)
    flows = cursor.fetchall()
    for flow in flows:
        print(flow[0])

except sqlite3.Error as error:
    print("Error executing SQL query:", error)

finally:
    # Close connection
    cursor.close()
    connection.close()
