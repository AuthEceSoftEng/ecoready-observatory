import paho.mqtt.client as mqtt
from confluent_kafka import Producer
import time
import json

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:59092',
    'client.id': 'weather-to-kafka-producer',
    "security.protocol": "sasl_plaintext",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "alice",
    "sasl.password": "alice-secret"
}

producer = Producer(conf)
# Callback when MQTT client is connected
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker on port {client.port} with result code {rc}")
    client.subscribe(mqtt_topic)

# Callback when MQTT client receives a message
def on_message(client, userdata, msg):
    global message_counts

    if message_counts[client.port] < 200:  # Limit to 10 messages per broker
        print(f"Received message from topic: {msg.topic}")
        print(f"Message payload: {msg.payload.decode()}")

        # Parse the received JSON message
        try:
            message_data = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            print("Failed to parse JSON message.")
            return

        # Add a "timestamp" key-value pair
        message_data["timestamp"] = int(time.time()*1000)

        # Convert the modified message_data back to JSON
        modified_message = json.dumps(message_data)

        # Calculate the key based on the broker's port, ranging from 1 to 20
        key = client.port - 1983  # Adjust to start from 1

        # Publish the modified message to Kafka with the calculated key
        producer.produce('test98', key=str(key), value=modified_message)
        producer.flush()

        message_counts[client.port] += 1

# Initialize message counts for each broker
message_counts = {}

# Loop to connect to MQTT brokers on ports 1984 to 2003
for port in range(1984,1985):
    mqtt_broker_host = "localhost"
    mqtt_broker_port = port
    mqtt_topic = "smauto/bme"

    # Create an MQTT client for this broker
    client = mqtt.Client()
    client.port = mqtt_broker_port
    client.on_connect = on_connect
    client.on_message = on_message
\
    # Initialize message count for this broker
    message_counts[client.port] = 0

    # Connect to the MQTT broker
    client.connect(mqtt_broker_host, mqtt_broker_port, 60)

    # Start the MQTT client loop to process and send messages to Kafka
    client.loop_start()

# Keep the script running
while True:
    pass
