from cassandra.cluster import Cluster
# Cassandra configuration
cassandra_host = 'localhost'  # Replace with your Cassandra host
keyspace = 'weather_data_2'
table = 'weather_table'

# Connect to the Cassandra cluster
cluster = Cluster([cassandra_host])
session = cluster.connect()

# Create a keyspace if not exists
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS weather_data_2
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Use the keyspace
session.set_keyspace('weather_data_2')

# Create a table. Clustering order by timestamp
table_creation_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id TEXT,
        day DATE,
        timestamp TIMESTAMP,
        temperature FLOAT,
        humidity FLOAT,
        pressure FLOAT,
        wind_speed FLOAT,
        wind_direction FLOAT,
        precipitation FLOAT,
        cloud_cover FLOAT,
        PRIMARY KEY ((id, day), timestamp)
    ) WITH CLUSTERING ORDER BY (timestamp DESC)
"""
session.execute(table_creation_query)

# Close the connection
cluster.shutdown()
