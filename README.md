# Data Ingestion Pipeline

## Description
This repository contains a data ingestion pipeline that simulates real-time data processing and storage into a SQL Server database.

## Files
- `data_pipeline.py`: Script for data ingestion and processing.
- `records.csv`: Sample data for ingestion.
- `data_queries.py`: Script for querying the processed data from SQL Server.

## Setup
1. ** Install Dependencies: **
   ```bash
   pip install pandas pyodbc

2. ** Configure the Database Connection: **
- Open data_pipeline.py and data_queries.py, and update the connection strings with your SQL Server credentials.

3. ** Run the Data Pipeline Script: **
```bash
python data_pipeline.py

4. ** Run the Queries Script: **
- python data_queries.py

##Optimization

```markdown
To handle a larger volume of data and improve performance, consider the following optimizations:

### Database Optimization

- ** Indexes: **
  - Create an index on the `total_value` column to speed up filtering queries.
    ```sql
    CREATE INDEX idx_total_value ON aggregated_data(total_value);
    ```
  - Create an index on the `timestamp` column if you plan to query data based on dates.
    ```sql
    CREATE INDEX idx_timestamp ON aggregated_data(timestamp);
    ```

- ** Data Compression: **
  - Enable row-level compression to reduce table size and improve I/O performance.
    ```sql
    ALTER TABLE aggregated_data REBUILD WITH (DATA_COMPRESSION = ROW);
    ```

- ** Table Partitioning (Optional): **
  - Partition the table by date if it is expected to grow significantly.
    ```sql
    -- Example of partitioning by date
    ```

### Data Pipeline Optimization

- ** Batch Processing: **
  - Process data in batches instead of row by row to reduce the number of database operations.
    ```python
    import pandas as pd
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

    # Read data from a CSV file
    data = pd.read_csv('records.csv')

    # Batch processing
    batch_size = 100
    batch = []

    for index, row in data.iterrows():
        batch.append((row['user'], row['value'], pd.to_datetime(row['timestamp'])))
        
        if len(batch) >= batch_size:
            cursor.executemany("INSERT INTO aggregated_data ([user], total_value, timestamp) VALUES (?, ?, ?)", batch)
            conn.commit()
            batch = []

    if batch:
        cursor.executemany("INSERT INTO aggregated_data ([user], total_value, timestamp) VALUES (?, ?, ?)", batch)
        conn.commit()

    conn.close()
    ```

- ** Connection Management: **
  - Keep the connection open during the entire data processing to avoid the overhead of repeatedly opening and closing connections.

- ** Error Handling: **
  - Implement robust error handling to log and manage errors during data ingestion.


  ## Queries

The `data_queries.py` file contains Python scripts for:

- ** Aggregated Summary: ** Fetching the total and average of `total_value`.
- ** Data Retrieval: ** Retrieving records where `total_value` is greater than 100.

## Future Improvements

- ** Scalability: ** Consider using Apache Spark for distributed processing of larger datasets. **
- ** Data Validation: ** Add validation steps to ensure data integrity before ingestion. **
- ** Real-time Streaming: ** Explore real-time streaming solutions like Apache Kafka for more accurate data **simulation. **
- ** Monitoring: ** Implement logging and monitoring for pipeline performance and error tracking.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
