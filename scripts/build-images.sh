#!/bin/bash

# Set project image tags
FLINK_IMAGE_TAG="custom-flink-image"
KAFKA_TO_CASSANDRA_IMAGE_TAG="kafka-cassandra-consumer"
KAFKA_LIVE_IMAGE_TAG="kafka-live-consumer"

# Build Flink image
echo "Building custom Flink Docker image..."
cd ./flink || exit
docker build -t $FLINK_IMAGE_TAG .
cd - || exit

# Build Kafka-to-Cassandra consumer image
echo "Building Kafka-to-Cassandra consumer Docker image..."
cd ./kafka-to-cassandra || exit
docker build -t $KAFKA_TO_CASSANDRA_IMAGE_TAG .
cd - || exit

# Build Flink-to-Cassandra consumer image
echo "Building Kafka lice consumer Docker image..."
cd ./kafka-live-consumer || exit
docker build -t $KAFKA_LIVE_IMAGE_TAG .
cd - || exit

echo "All custom Docker images built successfully!"
