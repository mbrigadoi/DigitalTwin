from pathlib import Path
import sys
import json

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from generic.producer import GenericProducer

SERVER = "localhost:9092"
TOPIC = "flights"

flights = json.load(open("flights.json"))

flightProducer = GenericProducer(server=SERVER, topic=TOPIC, data=flights)
flightProducer.produce()
