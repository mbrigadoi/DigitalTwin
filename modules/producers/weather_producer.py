from producer import GenericProducer


SERVER = "localhost:9092"
TOPIC = "weather"

WHEATHER_MOCK = [
    {
        "id": "1",
        "main": "Clear",
        "sunrise": "2024-02-07 07:30:00",
        "sunset": "2024-02-07 17:45:00",
        "temperature": 15.0,
        "perceivedTemperature": 14.5,
        "pressure": 1013.0,
        "humidity": 56.0,
        "visibility": 10.0,
        "windSpeed": 3.2,
        "windDegree": 180.0,
    },
    {
        "id": "2",
        "main": "Clouds",
        "sunrise": "2024-02-08 07:31:00",
        "sunset": "2024-02-08 17:46:00",
        "temperature": 16.0,
        "perceivedTemperature": 15.5,
        "pressure": 1012.0,
        "humidity": 58.0,
        "visibility": 9.0,
        "windSpeed": 3.5,
        "windDegree": 190.0,
    },
    {
        "id": "3",
        "main": "Rain",
        "sunrise": "2024-02-09 07:32:00",
        "sunset": "2024-02-09 17:47:00",
        "temperature": 14.0,
        "perceivedTemperature": 13.5,
        "pressure": 1011.0,
        "humidity": 60.0,
        "visibility": 8.0,
        "windSpeed": 3.8,
        "windDegree": 200.0,
    },
    {
        "id": "4",
        "main": "Snow",
        "sunrise": "2024-02-10 07:33:00",
        "sunset": "2024-02-10 17:48:00",
        "temperature": 0.0,
        "perceivedTemperature": -1.0,
        "pressure": 1010.0,
        "humidity": 62.0,
        "visibility": 7.0,
        "windSpeed": 4.0,
        "windDegree": 210.0,
    },
    {
        "id": "5",
        "main": "Fog",
        "sunrise": "2024-02-11 07:34:00",
        "sunset": "2024-02-11 17:49:00",
        "temperature": 8.0,
        "perceivedTemperature": 7.5,
        "pressure": 1009.0,
        "humidity": 64.0,
        "visibility": 6.0,
        "windSpeed": 4.2,
        "windDegree": 220.0,
    },
]


class WeatherProducer(GenericProducer):
    def __init__(self, server, topic, data):
        super().__init__(server, topic, data)


if __name__ == "__main__":
    weatherProducer = WeatherProducer(SERVER, TOPIC, WHEATHER_MOCK)
    weatherProducer.produce()
