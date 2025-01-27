# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV KAFKA_BOOTSTRAP_SERVERS=${KAFKA_BOOTSTRAP_SERVERS:-localhost:59096}
ENV COLLECTION_NAME=your_collection_name
ENV PROJECT_NAME=your_project_name
ENV ORGANIZATION_NAME=your_organization_name
ENV GROUP_ID=your_group_id

# Set the default command for the container
CMD ["python", "consumer.py"]
