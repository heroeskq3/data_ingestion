import pandas as pd
import time
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

# Create a table if it doesn't exist
cursor.execute('''
    IF OBJECT_ID('dbo.aggregated_data', 'U') IS NULL
    CREATE TABLE aggregated_data (
        [user] NVARCHAR(100),
        total_value FLOAT,
        timestamp DATETIME
    )
''')
conn.commit()

# Read data from a CSV file (simulating real-time data ingestion)
data = pd.read_csv('records.csv')

# Simulate real-time ingestion and basic processing
for index, row in data.iterrows():
    print(f"Ingesting: {row.to_dict()}")
    
    # Filter if the value is greater than 100
    if row['value'] > 100:
        # Insert processed data into the table
        cursor.execute(
            "INSERT INTO aggregated_data ([user], total_value, timestamp) VALUES (?, ?, ?)",
            row['user'],
            row['value'],
            pd.to_datetime(row['timestamp'])  # Convert timestamp to datetime format
        )
        conn.commit()
    
    time.sleep(5)  # Simulates the arrival of new data every second

# Close the connection
conn.close()
