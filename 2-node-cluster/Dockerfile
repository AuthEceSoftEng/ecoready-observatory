FROM flink:1.19.0

# Install python3, pip3, and wget
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev wget && rm -rf /var/lib/>

RUN ln -s /usr/bin/python3 /usr/bin/python

# Install PyFlink
RUN pip3 install apache-flink==1.19.0

# Download the JAR file using wget
RUN wget -O /opt/flink/lib/flink-sql-connector-kafka-3.0.2-1.18.jar https://rep>

