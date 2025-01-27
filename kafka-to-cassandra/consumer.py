import os
from confluent_kafka import Consumer, KafkaError, KafkaException
from cassandra.cluster import Cluster
import json

# Kafka and Cassandra configurations from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
CASSANDRA_CONTACT_POINTS = [os.getenv('CASSANDRA_CONTACT_POINTS', 'localhost')]
CASSANDRA_PORT = int(os.getenv('CASSANDRA_PORT', '9042'))
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'your_collection_name')
PROJECT_NAME = os.getenv('PROJECT_NAME', 'your_project_name')
ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME', 'your_organization_name')

# Cassandra setup
cluster = Cluster(CASSANDRA_CONTACT_POINTS, port=CASSANDRA_PORT)
session = cluster.connect()

def consume_and_store(topic_name, keyspace_name, table_name):
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': f"{topic_name}_cassandra_writer",
        'auto.offset.reset': 'earliest'
    })
    
    consumer.subscribe([topic_name])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        else:
            message_data = json.loads(msg.value().decode('utf-8'))
            message_data['key'] = msg.key().decode('utf-8') if msg.key() else None
            # Construct insert query
            columns = ', '.join(message_data.keys())
            placeholders = ', '.join(['%s'] * len(message_data))
            query = f"INSERT INTO {keyspace_name}.{table_name} ({columns}) VALUES ({placeholders})"
            session.execute(query, list(message_data.values()))

if __name__ == "__main__":
    topic = f"{ORGANIZATION_NAME}.{PROJECT_NAME}.{COLLECTION_NAME}"
    table = f"{PROJECT_NAME}_{COLLECTION_NAME}"
    consume_and_store(topic, ORGANIZATION_NAME, table)
