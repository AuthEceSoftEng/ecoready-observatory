from confluent_kafka import Consumer, KafkaError
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import json,time

# Kafka configuration
kafka_config = {
    'bootstrap.servers': 'localhost:59092',
    'group.id': 'cassandra-weather-data-consumer-group',
    'auto.offset.reset': 'latest',
    'auto.commit.interval.ms': 50,
    "security.protocol": "sasl_plaintext",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "alice",
    "sasl.password": "alice-secret"
}

# Cassandra configuration
cassandra_host = 'localhost'
keyspace = 'weather_data_2'
table = 'weather_table'

# Create Kafka consumer instance
consumer = Consumer(kafka_config)

# Subscribe to the Kafka topic
consumer.subscribe(['test98'])

# Create Cassandra session
cluster = Cluster([cassandra_host])
session = cluster.connect(keyspace)

batch_size = 150
batch = None
batch_timeout = 30  # Set the batch timeout to 30 seconds
last_batch_time = time.time()  # Initialize the last batch time

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        if batch is not None and (time.time() - last_batch_time) >= batch_timeout:
            session.execute(batch)
            print(f"Inserted batch of {len(batch)} records into Cassandra")
            batch = None
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    try:
        key = msg.key().decode()
        value = msg.value().decode()
        message_data = json.loads(value)

        if batch is None:
            batch = BatchStatement()

        # Extract data from the Kafka message
        id = 1  # You may set the appropriate 'id' value here
        day = time.strftime("%Y-%m-%d", time.gmtime(message_data['timestamp'] / 1000))  # Divide by 1000 to convert to seconds

        # Define the Cassandra query
        query = f"""
            INSERT INTO {table}
            (id, day, timestamp, temperature, humidity, pressure, wind_speed, wind_direction, precipitation, cloud_cover)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Prepare the query and bind parameters
        prepared_query = session.prepare(query)
        batch.add(prepared_query.bind([key, day, message_data['timestamp'], message_data['temperature'],
                                       message_data['humidity'], message_data['pressure'],
                                       message_data['wind_speed'], message_data['wind_direction'],
                                       message_data['precipitation'], message_data['cloud_cover']]))

        # Check if the batch size is reached
        if len(batch) >= batch_size or (((time.time() - last_batch_time) >= batch_timeout) and len(batch)>0):
            session.execute(batch)
            print(f"Inserted batch of {len(batch)} records into Cassandra")
            batch = None
            last_batch_time = time.time()  # Update the last batch time
    except Exception as e:
        print("Processing failed:", e)
        pass

consumer.close()
session.shutdown()
cluster.shutdown()
