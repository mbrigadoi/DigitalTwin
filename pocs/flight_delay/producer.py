import json
from datetime import datetime

from FlightRadar24 import FlightRadar24API

# Create an instance of FlightRadar24API
fr = FlightRadar24API()

airportData = fr.get_airport_details('LFPG')

schedule = []

for flight in airportData['airport']['pluginData']['schedule']['arrivals']['data']:
        flight = flight['flight']
        arr = None
        if flight['status']['generic']['status']['text'] != "canceled":
            arr = flight['time']['real']['arrival'] if flight['status']['generic']['status']['text'] == "landed" else flight['time']['estimated']['arrival']
        schedule.append({
            'flight': flight['identification']['number']['default'],
            'aircraft': flight['aircraft']['model']['text'],
            'airline': flight['airline']['short'],
            'origin': flight['airport']['origin']['name'],
            'status': flight['status']['text'],
            'scheduledDepartureGMT': datetime.utcfromtimestamp(flight['time']['scheduled']['departure'] + flight['airport']['destination']['timezone']['offset']).strftime('%Y-%m-%d %H:%M:%S'),
            'scheduledArrivalGMT': datetime.utcfromtimestamp(flight['time']['scheduled']['arrival'] + flight['airport']['destination']['timezone']['offset']).strftime('%Y-%m-%d %H:%M:%S'),
            'arrivalGMT': datetime.utcfromtimestamp(arr + flight['airport']['destination']['timezone']['offset']).strftime('%Y-%m-%d %H:%M:%S') if arr else "CANCELED"
        })

with open("airport.json", "w") as file:
    json.dump(airportData, file, indent=4)  

with open("schedule.json", "w") as file:
    json.dump(schedule, file, indent=4)