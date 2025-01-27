import os
from confluent_kafka import Consumer, KafkaError

# Kafka configurations from environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9096')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'your_collection_name')
PROJECT_NAME = os.getenv('PROJECT_NAME', 'your_project_name')
ORGANIZATION_NAME = os.getenv('ORGANIZATION_NAME', 'your_organization_name')
GROUP_ID = os.getenv('GROUP_ID', f"{PROJECT_NAME}.{COLLECTION_NAME}_live_group")

def get_kafka_consumer():
    return Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'latest'
    })

def consume_and_broadcast(consumer, topic):
    consumer.subscribe([topic])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
        else:
            # Placeholder for broadcasting the message
            print(f"Received message: {msg.value().decode('utf-8')}")

if __name__ == "__main__":
    consumer = get_kafka_consumer()
    topic = f"{ORGANIZATION_NAME}.{PROJECT_NAME}.{COLLECTION_NAME}"
    consume_and_broadcast(consumer, topic)
