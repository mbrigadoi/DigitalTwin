import os
from pathlib import Path
from datetime import datetime

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings, DataTypes, Row
from pyflink.common.typeinfo import Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.table.udf import FunctionContext
from pyflink.datastream.functions import ProcessFunction
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer

from business_rules.engine import when, then

# Define the business rule threshold
delay_threshold = 5

# Define a function to calculate the hour from a timestamp
def get_hour(timestamp):
    return datetime.fromisoformat(timestamp).hour

# Business rule function to detect delays within an hour
def flight_delay_rule(context):
    return when(lambda data: data["delay"] > 0) \
           .then(lambda data: data.update({"delay_minute": data["delay"]}))

# Flink function to process flight data, apply rules, and store in dict
class FlightDelayFunction(ProcessFunction):

    def __init__(self):
        self.delays_by_hour = {}

    def open(self, context: FunctionContext) -> None:
        pass

    def process_element(self, value: Row, context: FunctionContext) -> None:
        # Apply business rule to calculate delay minutes
        rule_result = flight_delay_rule(value.asDict())
        if rule_result is not None:
            value["delay_minute"] = rule_result["delay_minute"]

        # Extract hour from timestamp
        hour = get_hour(value["arrival_time"])

        # Update delays for the current hour
        self.delays_by_hour[hour] = self.delays_by_hour.get(hour, 0) + 1

        # Check if delay threshold is met and send alert to another topic (simulated here)
        if self.delays_by_hour[hour] > delay_threshold:
            alert_message = f"Alert: {self.delays_by_hour[hour]} flights delayed in hour {hour}"
            print(f"Sending alert: {alert_message}")  # Simulate sending to another Kafka topic

    def close(self) -> None:
        pass

def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()

    # Create table environment
    tblEnv = StreamTableEnvironment.create(
        stream_execution_environment=env, environment_settings=settings
    )

    # Add kafka connector dependency
    kafkaConn = os.path.join(
        os.path.abspath(f"{Path(__file__).parents[1]}/generic"),
        "flink-sql-connector-kafka-3.0.2-1.18.jar",
    )

    tblEnv.get_config().get_configuration().set_string(
        "pipeline.jars", "file://{}".format(kafkaConn)
    )

    # Create Kafka Source Table with DDL
    flightsDdl = """
        CREATE TABLE flights (
            flight VARCHAR(255),
            aircraft VARCHAR(255),
            airline VARCHAR(255),
            origin VARCHAR(255),
            status VARCHAR(255),
            scheduledDepartureGMT TIMESTAMP,
            scheduledArrivalGMT TIMESTAMP,
            arrivalGMT TIMESTAMP
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'flights',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flights',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """

    tblEnv.execute_sql(flightsDdl)

    # Create and initiate loading of source Table
    tblFlights = tblEnv.from_path("flights")

    print("\nSource Schema")
    tblFlights.print_schema()

    # Execute the SQL query
    query = """
        SELECT
            extract(HOUR FROM scheduled_arrival_gmt) AS hour,
            COUNT(*) AS late_or_canceled_count
        FROM flights
        WHERE status IN ('Late', 'Canceled')
    """

    sinkTable = tblEnv.sql_query(query)
    # Convert the Table into a DataStream
    dataStream = tblEnv.to_append_stream(
        sinkTable, Types.ROW([Types.SQL_TIMESTAMP(), Types.LONG()])
    )

    # Filter the DataStream
    filteredStream = dataStream.filter(lambda row: row[1] > 5)

    # Convert the filtered DataStream back into a Table
    filteredTable = tblEnv.from_data_stream(filteredStream)

    # Convert the filtered DataStream to string
    stringStream = filteredStream.map(lambda row: str(row), output_type=Types.STRING())

    # Define Kafka properties
    props = {"bootstrap.servers": "localhost:9092"}

    # Define Kafka sink
    kafka_sink = FlinkKafkaProducer(
        "delays", SimpleStringSchema(), props  # target topic  # serialization schema
    )  # kafka producer config

    stringStream.add_sink(kafka_sink)

    # Execute the job
    env.execute("Send filtered data to Kafka")


if __name__ == "__main__":
    main()
