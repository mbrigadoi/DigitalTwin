# Select working directory
cd ~/Workspace/DigitalTwin

# Delete topics
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic weather
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flight_weather

# Teardown Kafka services
docker-compose down -v