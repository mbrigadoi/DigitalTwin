# Select working directory
cd ~/Workspace/DigitalTwin

# Run containers
docker-compose up -d
sleep 5
# Create topics
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic weather
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flight_weather

# Run producers and consumer
gnome-terminal --tab -- bash -c "source venv/bin/activate; python modules/producers/flights_producer.py; exec bash"
gnome-terminal --tab -- bash -c "source venv/bin/activate; python modules/producers/weather_producer.py; exec bash"
gnome-terminal --tab -- bash -c "source venv/bin/activate; python modules/consumers/consumer.py; exec bash"

# Run kafka-console-consumer
docker exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic flight_weather --from-beginning