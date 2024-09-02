import pyodbc

# Connect to SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=data_ingestion;'
    'UID=sa;'
    'PWD=Solid256!'
)
cursor = conn.cursor()

# Execute the first query (Aggregated Summary)
cursor.execute('''
    SELECT 
        SUM(total_value) AS TotalSum,
        AVG(total_value) AS AverageValue
    FROM aggregated_data
''')
summary = cursor.fetchone()
print("Aggregated Summary:")
print(f"Total Sum: {summary.TotalSum}")
print(f"Average Value: {summary.AverageValue}")

# Execute the second query (Retrieve Data where total_value > 100)
cursor.execute('''
    SELECT * 
    FROM aggregated_data
    WHERE total_value > 100
''')
results = cursor.fetchall()
print("\nData where total_value > 100:")
for row in results:
    print(row)

# Close the connection
conn.close()
