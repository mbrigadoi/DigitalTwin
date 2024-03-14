from pathlib import Path
import sys
import json

from random import shuffle

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from generic.producer import GenericProducer

SERVER = "localhost:9092"
TOPIC = "flights"
FILE = "/home/mbrigadoi/Workspace/DigitalTwin/pocs/flight_persistence/flights.json"

flights = json.load(
    open(FILE)
)

shuffle(flights)

flightProducer = GenericProducer(server=SERVER, topic=TOPIC, data=flights)
flightProducer.produce()
