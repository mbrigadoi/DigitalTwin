# Kafka setup
## Download and extract Kafka
curl https://dlcdn.apache.org/kafka/3.6.1/kafka_2.13-3.6.1.tgz --output kafka_2.13-3.6.1.tgz
tar xzf kafka_2.13-3.6.1.tgz
cd kafka_2.13-3.6.1.tgz
## Start Zookeeper 
### Start Zookeeper service
bin/zookeeper-server-start.sh config/zookeeper.properties
### Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties
## Create a topic
bin/kafka-topics.sh --create --topic test-events --bootstrap-server localhost:9092
### Display topic information
bin/kafka-topics.sh --describe --topic test-events --bootstrap-server localhost:9092
## Write events into the topic
bin/kafka-console-producer.sh --topic test-events --bootstrap-server localhost:9092
## Read events of the topic
bin/kafka-console-consumer.sh --topic test-events --from-beginning --bootstrap-server localhost:9092

# Flink setup
## Download and extract Flink
curl https://dlcdn.apache.org/flink/flink-1.18.1/flink-1.18.1-bin-scala_2.12.tgz --output flink-1.18.1-bin-scala_2.12.tgz
tar xzf flink-1.18.1-bin-scala_2.12.tgz
cd flink-1.18.1
## Start Flink
bin/start-local.sh
## Submit a Flink job (e.g. WordCount)
./bin/flink run examples/streaming/WordCount.jar
## Stop Flink
bin/stop-local.sh

# Container
## Setup docker-compose file for Kafka broker and Zookeeper
## Download flink sql connector for Kafka
curl https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar --output flink-sql-connector-kafka-3.0.2-1.18.jar
## Run Kafka broker and Zookeeper
docker-compose up -d
## Create a topic
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic flights
docker exec -it broker kafka-topics --create --bootstrap-server localhost:9092 --topic weather
## Run the producers
### It can be a python script or a java application
python flights_producer.py
python weather_producer.py
## Run the consumers 
### It can be a python script or a java application
python consumer.py
## Enable the data flow from the producers to the consumers
docker exec -it broker kafka-console-consumer --bootstrap-server localhost:9092 --topic flight_weather --from-beginning
## Cleanup
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic flights
docker exec -it broker kafka-topics --delete --bootstrap-server localhost:9092 --topic weather
docker-compose down -v
