import sqlite3

# Connect to SQLite
connection = sqlite3.connect('flows.db')
# Create a cursor object
cursor = connection.cursor()

#example F
F = "Decimal to Dash"
try:
    #query
    query = f"SELECT core_nodes, other_nodes FROM flows WHERE name = ?"
    cursor.execute(query, (F,))
    result = cursor.fetchone()

    #result
    if result:
        core_nodes = result[0]
        other_nodes = result[1]

        # print
        print("Core Nodes:", core_nodes)
        print("Other Nodes:", other_nodes)
    else:
        print("Flow not found with the specified name:", F)

except sqlite3.Error as error:
    print("Error executing SQL query:", error)

finally:
    # Close connection
    cursor.close()
    connection.close()
