from confluent_kafka import Consumer, KafkaError
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import json
import time
from datetime import datetime

# Kafka configuration
kafka_config = {
    'bootstrap.servers': 'localhost:59092',  # Update with your Kafka broker address
    'group.id': 'flink-hourly-eeris-aggr2',
    'auto.offset.reset': 'earliest',
    'auto.commit.interval.ms': 50,
    "security.protocol": "sasl_plaintext",  # Use SASL_PLAINTEXT
    "sasl.mechanism": "PLAIN",  # Use PLAIN SASL mechanism
    "sasl.username": "alice",
    "sasl.password": "alice-secret"
}

# Cassandra configuration
cassandra_host = 'localhost'  # Update with your Cassandra host
keyspace = 'eeris_flink_aggregations'
aggr_table = 'hourly_aggregations2'

# Create Kafka consumer instance
consumer = Consumer(kafka_config)

# Subscribe to the Kafka topic for minute aggregations
consumer.subscribe(['1hour_eeris_flink_aggregation2'])

# Create Cassandra session
cluster = Cluster([cassandra_host])
session = cluster.connect(keyspace)

def get_day_from_timestamp(timestamp):
 #   timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return timestamp.date()

while True:
    msg = consumer.poll(0.5)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(34)
            print(msg.error())
            break

    try:
        message_data = json.loads(msg.value().decode('utf-8'))

        # Convert 'window_start' and 'window_end' to datetime objects
        window_start_dt = datetime.strptime(message_data['window_start'], "%Y-%m-%d %H:%M:%S")
        window_end_dt = datetime.strptime(message_data['window_end'], "%Y-%m-%d %H:%M:%S")
#        print(type(message_data['window_start']),type(message_data['window_end']),type(window_start_dt),type(window_end_dt))
        # Calculate 'day' from 'window_start'
        day = get_day_from_timestamp(window_start_dt)  # Pass datetime object instead of string

        # Define the Cassandra query
        query = f"""
            INSERT INTO {aggr_table}
            (key, day, window_start, window_end, count, avg_p, max_p, min_p, avg_q, max_q, min_q, avg_i, max_i, min_i, avg_v, max_v, min_v, avg_f, max_f, min_f)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Prepare the query and bind parameters
        prepared_query = session.prepare(query)
        session.execute(prepared_query.bind([message_data['key'], day, window_start_dt, 
                                       window_end_dt, message_data['count'],
                                       message_data['avg_p'], message_data['max_p'], message_data['min_p'],
                                       message_data['avg_q'], message_data['max_q'], message_data['min_q'],
                                       message_data['avg_i'], message_data['max_i'], message_data['min_i'],
                                       message_data['avg_v'], message_data['max_v'], message_data['min_v'],
                                       message_data['avg_f'], message_data['max_f'], message_data['min_f']]))
    except Exception as e:
        print("Processing failed:", e)
        pass
print(1)
consumer.close()
session.shutdown()
cluster.shutdown()
