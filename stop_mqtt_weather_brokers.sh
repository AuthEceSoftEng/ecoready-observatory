#!/bin/bash
container_name="emqx_1"
# Stop and remove the Docker container by name
docker stop "$container_name"
echo "Docker containers have been stopped and removed."

