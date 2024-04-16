#!/bin/bash

# Number of times to run the command
count=2

# Base port for MQTT
mqtt_base_port=1984

# Base port for EMQ X dashboard
dashboard_base_port=18084

# Calculate the ports and container name for this iteration
mqtt_port=$((mqtt_base_port))
dashboard_port=$((dashboard_base_port))
container_name="emqx_1"
# Run the Docker command in the background with detached mode (-d)
docker run -d --rm --name "$container_name" -p "$dashboard_port:18083" -p "$mqtt_port:1883" emqx/emqx:latest

echo "Docker containers are running in the background."

