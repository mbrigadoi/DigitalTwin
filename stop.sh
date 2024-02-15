# Select working directory
cd ~/Workspace/DigitalTwin

# Delete topics
# # Flight Weather
# docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
# docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic weather
# docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flight_weather

# Flight Delay
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic delays

# Teardown Kafka services
docker-compose down -v