from cassandra.cluster import Cluster
# Cassandra configuration
cassandra_host = 'localhost'  # Replace with your Cassandra host
keyspace = 'eeris'
table = 'eeris_table'

# Connect to the Cassandra cluster
cluster = Cluster([cassandra_host])
session = cluster.connect()

# Create a keyspace if not exists
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS eeris
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Use the keyspace
session.set_keyspace('eeris')

# Create a table with FLOAT data types and clustering order by timestamp
table_creation_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        id TEXT,
        day DATE,
        prod_timestamp TIMESTAMP,
        ts BIGINT,
        p FLOAT,
        q FLOAT,
        i FLOAT,
        v FLOAT,
        f FLOAT,
        PRIMARY KEY ((id, day), prod_timestamp)
    ) WITH CLUSTERING ORDER BY (prod_timestamp DESC)
"""
session.execute(table_creation_query)

# Close the connection
cluster.shutdown()
