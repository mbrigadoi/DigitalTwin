import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()

    settings = (
        EnvironmentSettings.new_instance()
        .in_streaming_mode()
        .build()
    )

    # Create table environment
    tblEnv = StreamTableEnvironment.create(
        stream_execution_environment=env, environment_settings=settings
    )

    # Add kafka connector dependency
    kafkaConn = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "flink-sql-connector-kafka-3.0.2-1.18.jar",
    )

    tblEnv.get_config().get_configuration().set_string(
        "pipeline.jars", "file://{}".format(kafkaConn)
    )

    # Create Kafka Source Table with DDL
    flightsDdl = """
        CREATE TABLE flights (
            flightNumber VARCHAR(255),
            airline VARCHAR(255),
            departureAirport VARCHAR(255),
            departureCity VARCHAR(255),
            departureCountry VARCHAR(255),
            departureDateTime TIMESTAMP,
            arrivalAirport VARCHAR(255),
            arrivalCity VARCHAR(255),
            arrivalCountry VARCHAR(255),
            arrivalDateTime TIMESTAMP,
            aircraftModel VARCHAR(255),
            aircraftCapacity INT,
            statusDescription VARCHAR(255),
            statusReason VARCHAR(255),
            statusNewArrivalTime TIMESTAMP,
            weatherId INT
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'flights',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flights',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """

    weatherDdl = """
        CREATE TABLE weather (
            id INT,
            main VARCHAR(255),
            sunrise TIMESTAMP,
            sunset TIMESTAMP,
            temperature FLOAT,
            perceivedTemperature FLOAT,
            pressure FLOAT,
            humidity FLOAT,
            visibility FLOAT,
            windSpeed FLOAT,
            windDegree FLOAT
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'weather',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'weather',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        )
    """

    tblEnv.execute_sql(flightsDdl)
    tblEnv.execute_sql(weatherDdl)

    # Create and initiate loading of source Table
    tblFlights = tblEnv.from_path("flights")
    tblWeather = tblEnv.from_path("weather")

    print("\nSource Schema")
    tblFlights.print_schema()
    tblWeather.print_schema()

    # Define query for join and aggregation of flights and weather
    query = """
        SELECT 
            f.flightNumber,
            f.airline,
            f.departureCity,
            f.departureAirport,
            f.arrivalCity,
            f.arrivalAirport,
            f.departureDateTime AS departureTime,
            f.statusNewArrivalTime,
            f.statusDescription,
            w.main AS mainWeather,
            w.temperature,
            w.humidity,
            w.visibility,
            w.windSpeed,
            w.windDegree
        FROM 
            flights f
        JOIN 
            weather w ON f.weatherId = w.id;
    """
    sinkTable = tblEnv.sql_query(query)

    print("\nFlight_Weather Schema")
    sinkTable.print_schema()

    # Create the table combining the flights and weather data
    sinkDdl = """
        CREATE TABLE flight_weather (
            flightNumber VARCHAR(255),
            airline VARCHAR(255),
            departureCity VARCHAR(255),
            departureAirport VARCHAR(255),
            arrivalCity VARCHAR(255),
            arrivalAirport VARCHAR(255),
            departureTime TIMESTAMP,
            statusNewArrivalTime TIMESTAMP,
            statusDescription VARCHAR(255),
            mainWeather VARCHAR(255),
            temperature FLOAT,
            humidity FLOAT,
            visibility FLOAT,
            windSpeed FLOAT,
            windDegree FLOAT
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'flight_weather',
            'properties.bootstrap.servers' = 'localhost:9092',
            'format' = 'json'
        )
    """
    tblEnv.execute_sql(sinkDdl)

    # Write time windowed aggregations to sink table
    sinkTable.execute_insert("flight_weather").wait()

    tblEnv.execute("windowed-flight_weather")


if __name__ == "__main__":
    main()
