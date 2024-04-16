from cassandra.cluster import Cluster

# Cassandra configuration
cassandra_host = 'localhost'
keyspace = 'eeris'
table = 'eeris_table'

# Connect to the Cassandra cluster
cluster = Cluster([cassandra_host])
session = cluster.connect(keyspace)

# Drop the table
session.execute(f"DROP TABLE IF EXISTS {table};")

# Close the connection
cluster.shutdown()

