from kafka.admin import KafkaAdminClient, NewTopic, NewPartitions
from kafka import KafkaProducer

# Set Kafka broker configuration
bootstrap_servers = 'localhost:59092'

# Set the Kafka topic name
topic_name = 'eeris'

# Create Kafka AdminClient
admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers,security_protocol='SASL_PLAINTEXT', sasl_mechanism='PLAIN', sasl_plain_username='kafka', sasl_plain_password='pass123')

new_topic = NewTopic(name=topic_name, num_partitions=8, replication_factor=1)

# Create the topic
admin_client.create_topics(new_topics=[new_topic])
