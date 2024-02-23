from pathlib import Path
from pyflink.common.typeinfo import Types, RowTypeInfo
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()

    kafkaConn = os.path.join(
        os.path.abspath(f"{Path(__file__).parents[1]}/generic"),
        "flink-sql-connector-kafka-3.0.2-1.18.jar",
    )

    env.add_jars(f"file://{kafkaConn}")

    # Set up the Kafka consumer
    consumer = FlinkKafkaConsumer(
        "flights",  # The topic to consume
        SimpleStringSchema(),  # The schema for the data
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "test_group",
        },  # Kafka consumer properties
    )

    # Set up the Kafka producer
    producer = FlinkKafkaProducer(
        "delays",  # The topic to produce to
        SimpleStringSchema(),  # The schema for the data
        {"bootstrap.servers": "localhost:9092"},  # Kafka producer properties
    )

    # Create Kafka Source Table with DDL
    flightsDdl = """
        CREATE TABLE Flights (
            flight VARCHAR(255),
            aircraft VARCHAR(255),
            airline VARCHAR(255),
            origin VARCHAR(255),
            status VARCHAR(255),
            scheduledDepartureGMT TIMESTAMP,
            scheduledArrivalGMT TIMESTAMP,
            arrivalGMT TIMESTAMP,
            Delay TIME
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'flights',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flights',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """

    env.execute_sql(flightsDdl)

    # Create and initiate loading of source Table
    tblFlights = env.from_path("flights")

    print("\nSource Schema")
    tblFlights.print_schema()

    # Execute the SQL query
    result = t_env.sql_query("""
        SELECT HOUR(scheduledArrivalGMT) AS Hour, COUNT(*) AS DelayedOrCanceledFlights
        FROM Flights
        WHERE status = 'Estimated' OR status = 'Canceled'
        GROUP BY Hour
    """)

    # Convert the result to a DataStream
    result_ds = env.to_append_stream(result, result.get_schema().to_row_type())

    # For each result row, send it to a Kafka topic
    def send_to_kafka(row):
        producer.send('output_topic', value=row.as_dict())

    result_ds.add_sink(send_to_kafka)

    # Execute the Flink job
    env.execute("Flink Kafka producer")


if __name__ == "__main__":
    main()