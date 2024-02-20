import os
import json
from datetime import datetime
from pathlib import Path
from pyflink.common.typeinfo import Types, RowTypeInfo
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema


def main():
    # Set up the execution environment
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

    # Define the schema for your data
    schema = RowTypeInfo(
        [
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
            Types.LONG(),
            Types.STRING(),
        ],
        [
            "flight",
            "aircraft",
            "airline",
            "origin",
            "status",
            "scheduledDepartureGMT",
            "scheduledArrivalGMT",
            "arrivalGMT",
            "Delay",
        ],
    )

    # Read the data from Kafka
    stream = env.add_source(consumer)

    # Read the data from Kafka
    stream = stream.map(lambda s: json.loads(s), output_type=schema)

    # Check if the flight wasn't canceled and the difference of scheduledArrivalGMT and arrivalGMT is more than 10 minutes
    result = stream.filter(
        lambda row: row["arrivalGMT"] == -1
        or row["arrivalGMT"] - row["scheduledArrivalGMT"] > 600
    )

    # Convert the Unix timestamps to datetime strings
    result = result.map(
        lambda row: {
            "flight": row["flight"],
            "aircraft": row["aircraft"],
            "airline": row["airline"],
            "origin": row["origin"],
            "status": row["status"],
            "scheduledDepartureGMT": datetime.utcfromtimestamp(
                row["scheduledDepartureGMT"]
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "scheduledArrivalGMT": datetime.utcfromtimestamp(
                row["scheduledArrivalGMT"]
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "arrivalGMT": (
                datetime.utcfromtimestamp(row["arrivalGMT"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if row["arrivalGMT"] != -1
                else "CANCELED"
            ),
            "Delay": (
                datetime.utcfromtimestamp(
                    row["arrivalGMT"] - row["scheduledArrivalGMT"]
                ).strftime("%H:%M:%S")
                if row["arrivalGMT"] != -1
                else "CANCELED"
            ),
        },
        output_type=schema,
    )

    # Serialize the data to JSON
    result = result.map(lambda row: json.dumps(row), output_type=Types.STRING())

    # Write the results to Kafka
    result.add_sink(producer)

    # Execute the job
    env.execute("Flight Delay Checker")


if __name__ == "__main__":
    main()
