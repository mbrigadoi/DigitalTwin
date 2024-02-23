#!/bin/bash

# Check if the number of arguments is correct
if [ $# -eq 0 ]; then
    echo "Usage: ./run.sh <project> <docker|podman>"
    echo "Example: ./run.sh fw docker"
    exit 1
elif [ $# -gt 2 ]; then
    echo "Usage: ./run.sh <project> <docker|podman>"
    echo "Example: ./run.sh fw docker"
    exit 1
fi

# Check if project is valid
projects=("fw" "fd")
found=0

for i in "${projects[@]}"; do
    if [ "$i" == "$1" ]; then
        found=1
        break
    fi
done

if [ $found -eq 0 ]; then
    echo "Invalid project"
    echo "Valid projects: ${projects[@]}"
    exit 1
fi

# Select working directory
cd ~/Workspace/DigitalTwin

# Check if Docker or Podman is used
if [ "$2" == "docker" ]; then
    echo "Using Docker"
    CMD="docker "
else
    echo "Using Podman"
    CMD="podman"
fi

# Run containers
$CMD compose up -d 

# Check which project to run
if [ "$1" == "fw" ]; then
    # Flight Weather
    echo "Running Flight Weather project"
    # Create topics
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic weather
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flight_weather

    # Run producers and consumer
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_weather/producers/flights_producer.py; exec bash"
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_weather/producers/weather_producer.py; exec bash"
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_weather/consumers/consumer.py; exec bash"

    # Run kafka-console-consumer
    $CMD exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic flight_weather --from-beginning
elif [ "$1" == "fd" ]; then
    # Flight Delay
    echo "Running Flight Delay project"
    # Create topics
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic delays

    # Run producer and consumer
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_delay/producer.py; exec bash"
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_delay/consumer.py; exec bash"

    # Run kafka-console-consumer
    $CMD exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic delays --from-beginning
fi
elif [ "$1" == "fp" ]; then
    # Flight Delay
    echo "Running Flight Persistence project"
    # Create topics
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
    $CMD exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic delays

    # Run producer and consumer
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_persistence/producer.py; exec bash"
    gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_persistence/consumer.py; exec bash"

    # Run kafka-console-consumer
    $CMD exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic delays --from-beginning
fi