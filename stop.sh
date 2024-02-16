# Select working directory
cd ~/Workspace/DigitalTwin

# Delete topics
# # Flight Weather
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic weather
# podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flight_weather

# Flight Delay
podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
podman exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic delays

# Teardown Kafka services
podman compose down -v --remove-orphans