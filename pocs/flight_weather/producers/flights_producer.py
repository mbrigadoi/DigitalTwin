from producer import GenericProducer


SERVER = "localhost:9092"
TOPIC = "flights"

FLIGHTS_MOCK = [
    {
        "flightNumber": "AA123",
        "airline": "American Airlines",
        "departureAirport": "JFK",
        "departureCity": "New York",
        "departureCountry": "USA",
        "departureDateTime": "2024-02-09 10:00:00",
        "arrivalAirport": "LAX",
        "arrivalCity": "Los Angeles",
        "arrivalCountry": "USA",
        "arrivalDateTime": "2024-02-09 13:00:00",
        "aircraftModel": "Boeing 737",
        "aircraftCapacity": 200,
        "statusDescription": "On Time",
        "statusReason": "",
        "statusNewArrivalTime": "2024-02-09 13:00:00",
        "weatherId": "1",
    },
    {
        "flightNumber": "BA789",
        "airline": "British Airways",
        "departureAirport": "LHR",
        "departureCity": "London",
        "departureCountry": "UK",
        "departureDateTime": "2024-02-10 14:00:00",
        "arrivalAirport": "CDG",
        "arrivalCity": "Paris",
        "arrivalCountry": "France",
        "arrivalDateTime": "2024-02-10 16:00:00",
        "aircraftModel": "Airbus A320",
        "aircraftCapacity": 180,
        "statusDescription": "Delayed",
        "statusReason": "Technical Issue",
        "statusNewArrivalTime": "2024-02-10 16:30:00",
        "weatherId": "2",
    },
    {
        "flightNumber": "LH456",
        "airline": "Lufthansa",
        "departureAirport": "FRA",
        "departureCity": "Frankfurt",
        "departureCountry": "Germany",
        "departureDateTime": "2024-02-11 15:00:00",
        "arrivalAirport": "MUC",
        "arrivalCity": "Munich",
        "arrivalCountry": "Germany",
        "arrivalDateTime": "2024-02-11 16:00:00",
        "aircraftModel": "Airbus A380",
        "aircraftCapacity": 853,
        "statusDescription": "On Time",
        "statusReason": "",
        "statusNewArrivalTime": "2024-02-11 16:00:00",
        "weatherId": "3",
    },
    {
        "flightNumber": "DL456",
        "airline": "Delta Airlines",
        "departureAirport": "ATL",
        "departureCity": "Atlanta",
        "departureCountry": "USA",
        "departureDateTime": "2024-02-08 09:00:00",
        "arrivalAirport": "LHR",
        "arrivalCity": "London",
        "arrivalCountry": "UK",
        "arrivalDateTime": "2024-02-08 20:00:00",
        "aircraftModel": "Airbus A330",
        "aircraftCapacity": 250,
        "statusDescription": "Delayed",
        "statusReason": "Weather",
        "statusNewArrivalTime": "2024-02-08 21:00:00",
        "weatherId": "4",
    },
    {
        "flightNumber": "EK321",
        "airline": "Emirates",
        "departureAirport": "DXB",
        "departureCity": "Dubai",
        "departureCountry": "UAE",
        "departureDateTime": "2024-02-12 20:00:00",
        "arrivalAirport": "SYD",
        "arrivalCity": "Sydney",
        "arrivalCountry": "Australia",
        "arrivalDateTime": "2024-02-13 18:00:00",
        "aircraftModel": "Boeing 777",
        "aircraftCapacity": 396,
        "statusDescription": "Delayed",
        "statusReason": "Air Traffic",
        "statusNewArrivalTime": "2024-02-13 18:30:00",
        "weatherId": "5",
    },
]


class FlightProducer(GenericProducer):
    def __init__(self, server, topic, data):
        super().__init__(server, topic, data)


if __name__ == "__main__":
    flightProducer = FlightProducer(SERVER, TOPIC, FLIGHTS_MOCK)
    flightProducer.produce()
