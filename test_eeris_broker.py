import paho.mqtt.client as mqtt

# MQTT configuration
mqtt_broker = "livinglab.ee.auth.gr"
mqtt_port = 9001
mqtt_username = "etsardou"
mqtt_password = "topsecret"

# MQTT Topics to subscribe to
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

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    for topic in topics:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode('utf-8')}")

# Create and configure the MQTT client
client = mqtt.Client(transport="websockets")
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

# Start the MQTT loop
client.loop_forever()

