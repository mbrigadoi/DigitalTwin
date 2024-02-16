# Select working directory
cd ~/Workspace/DigitalTwin

# Run containers
podman compose up -d 

# Flight Weather
# # Create topics
# podman exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
# podman exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic weather
# podman exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flight_weather

# # Run producers and consumer
# gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_weather/producers/flights_producer.py; exec bash"
# gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_weather/producers/weather_producer.py; exec bash"
# gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_weather/consumers/consumer.py; exec bash"

# # Run kafka-console-consumer
# podman exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic flight_weather --from-beginning

# Flight Delay
# Create topics
podman exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
podman exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic delays

# Run producer and consumer
gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_delay/producer.py; exec bash"
gnome-terminal --tab -- bash -c "source venv/bin/activate; python pocs/flight_delay/consumer.py; exec bash"

# Run kafka-console-consumer
podman exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic flight_weather --from-beginning