import atexit
import json
import logging
import random
import time
import sys

from confluent_kafka import Producer

logging.basicConfig(
  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
  handlers=[
      logging.FileHandler("producers.log"),
      logging.StreamHandler(sys.stdout)
  ]
)

logger = logging.getLogger()

class ProducerCallback:
    def __init__(self, topic, record, log_success=False):
        self.record = record
        self.log_success = log_success

    def __call__(self, err, msg):
        if err:
            logger.error("Error producing record {}".format(self.record))
        elif self.log_success:
            logger.info(
                "Produced {} to topic {} partition {} offset {}".format(
                    self.record, msg.topic(), msg.partition(), msg.offset()
                )
            )


class GenericProducer:
    def __init__(self, server, topic, data):
        self.topic = topic
        self.data = data
        self.producer = Producer(
            {
                "bootstrap.servers": server,
                "linger.ms": 200,
                "client.id": f"{topic}_producer",
                "partitioner": "murmur2_random",
            }
        )
        atexit.register(lambda p: p.flush(), self.producer)

    def produce(self):
        logger.info(f"Starting {self.topic} producer")

        i = 1
        while True:
            is_tenth = i % 10 == 0

            data = random.choice(self.data)

            self.producer.produce(
                topic=self.topic,
                value=json.dumps(data),
                on_delivery=ProducerCallback(self.topic, data, log_success=is_tenth),
            )

            if is_tenth:
                self.producer.poll(1)
                time.sleep(5)
                i = 0

            i += 1
