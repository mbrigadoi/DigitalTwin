#!/bin/bash

# Check if Docker or Podman is used
if [ "$1" == "docker" ]; then
    echo "Using Docker"
    CMD="docker "
else
    echo "Using Podman"
    CMD="podman"
fi

# Select working directory
cd ~/Workspace/DigitalTwin

# Delete topics
TOPICS=$($CMD exec broker bash -c "kafka-topics --list --bootstrap-server localhost:9092" )

for T in $TOPICS
do
    $CMD exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic $T
done

# Teardown Kafka services
$CMD compose down -v --remove-orphans
