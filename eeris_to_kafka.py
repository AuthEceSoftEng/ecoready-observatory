import paho.mqtt.client as mqtt
from confluent_kafka import Producer
import json,time

# Kafka configuration
conf = {
    'bootstrap.servers': 'localhost:59092',
    'client.id': 'mqtt-to-kafka-producer',
    "security.protocol": "sasl_plaintext",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "alice",
    "sasl.password": "alice-secret"
}

producer = Producer(conf)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    topics = [
        "eeris/5f05d5d83a442d4f78db0a04",
        "eeris/5e05d5c83e442d4f78db036f",
        "eeris/5e05d6583e442d4f78db0371",
        "eeris/5e05d6583e442d4f78db0372",
        "eeris/5e05d6583e442d4f78db0373",
        "eeris/5e05d6583e442d4f78db0374",
        "eeris/5e05d6583e442d4f78db0375",
        "eeris/5e05d6583e442d4f78db0376"
    ]
    for topic in topics:
        client.subscribe(topic)

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    kafka_key = msg.topic[-3:]
    # Convert byte string to JSON string
    message_data = json.loads(msg.payload.decode('utf-8'))

    # Add a "prod_timestamp" key-value pair
    message_data["prod_timestamp"] = int(time.time() * 1000)
    # Convert the updated data back to JSON string
    json_value = json.dumps(message_data)

    # Produce the JSON string to Kafka
    producer.produce('eeris', key=kafka_key, value=json_value)

client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("etsardou", "topsecret")
client.connect("livinglab.ee.auth.gr", 9001, 60)

# Start the MQTT loop
client.loop_start()

# Run the Kafka producer loop to ensure messages are delivered
try:
    while True:
        producer.poll(0.5)
except KeyboardInterrupt:
    pass

# Stop the MQTT loop
client.loop_stop()

