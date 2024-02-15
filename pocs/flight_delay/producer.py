import json

from FlightRadar24 import FlightRadar24API

from producer import Producer

SERVER = "localhost:9092"
TOPIC = "weather"

# Create an instance of FlightRadar24API
fr = FlightRadar24API()

airportData = fr.get_airport_details("LFPG")

schedule = []

for flight in airportData["airport"]["pluginData"]["schedule"]["arrivals"]["data"]:
    flight = flight["flight"]
    arr = None
    if flight["status"]["generic"]["status"]["text"] != "canceled":
        arr = (
            flight["time"]["real"]["arrival"]
            if flight["status"]["generic"]["status"]["text"] == "landed"
            else flight["time"]["estimated"]["arrival"]
        )
    schedule.append(
        {
            "flight": flight["identification"]["number"]["default"],
            "aircraft": flight["aircraft"]["model"]["text"],
            "airline": flight["airline"]["short"],
            "origin": flight["airport"]["origin"]["name"],
            "status": flight["status"]["text"],
            "scheduledDepartureGMT": flight["time"]["scheduled"]["departure"]
            + flight["airport"]["destination"]["timezone"]["offset"],
            "scheduledArrivalGMT": flight["time"]["scheduled"]["arrival"]
            + flight["airport"]["destination"]["timezone"]["offset"],
            "arrivalGMT": (
                arr + flight["airport"]["destination"]["timezone"]["offset"]
                if arr
                else -1
            ),
        }
    )

with open("airport.json", "w") as file:
    json.dump(airportData, file, indent=4)

with open("schedule.json", "w") as file:
    json.dump(schedule, file, indent=4)

scheduleProducer = Producer(SERVER, TOPIC, schedule)
scheduleProducer.produce()
