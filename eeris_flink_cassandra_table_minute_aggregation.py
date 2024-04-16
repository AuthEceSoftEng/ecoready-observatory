from cassandra.cluster import Cluster
from datetime import datetime
from cassandra.query import SimpleStatement

# Cassandra configuration
cassandra_host = 'localhost'
keyspace = 'eeris_flink_aggregations'
table = 'minute_aggregations2'

# Connect to the Cassandra cluster
cluster = Cluster([cassandra_host])
session = cluster.connect()

# Create a keyspace if not exists
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS eeris_flink_aggregations
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Use the keyspace
session.set_keyspace('eeris_flink_aggregations')

# Create a table for minute aggregations
table_creation_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        key TEXT,
        day DATE,
        window_start TIMESTAMP,
        window_end TIMESTAMP,
        count INT,
        avg_p FLOAT,
        max_p FLOAT,
        min_p FLOAT,
        avg_q FLOAT,
        max_q FLOAT,
        min_q FLOAT,
        avg_i FLOAT,
        max_i FLOAT,
        min_i FLOAT,
        avg_v FLOAT,
        max_v FLOAT,
        min_v FLOAT,
        avg_f FLOAT,
        max_f FLOAT,
        min_f FLOAT,
        PRIMARY KEY ((key, day), window_start)
    ) WITH CLUSTERING ORDER BY (window_start ASC)
"""
session.execute(SimpleStatement(table_creation_query))
