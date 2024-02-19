#!/bin/bash

# Check if the number of arguments is correct
if [ "$1" == "docker" ]; then
    echo "Using Docker"
    CMD="docker "
else
    echo "Using Podman"
    CMD="podman"
fi

# Select working directory
cd ~/Workspace/DigitalTwin

TOPICS=$($CMD exec broker bash -c "kafka-topics --list --bootstrap-server localhost:9092" )

for T in $TOPICS
do
    $CMD exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic $T
done

# Delete topics
# # Flight Weather
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic weather
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flight_weather

# Flight Delay
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic delays

# Teardown Kafka services
$CMD compose down -v --remove-orphans
