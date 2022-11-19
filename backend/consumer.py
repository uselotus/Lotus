"""
A basic example of a Redpanda consumer
"""
import os
from dataclasses import dataclass

from kafka import KafkaConsumer

KAFKA_HOST = os.environ.get("KAFKA_HOST", "localhost")
EVENTS_TOPIC = os.environ.get("EVENTS_TOPIC", "events_topic")


@dataclass
class ConsumerConfig:
    bootstrap_servers = [KAFKA_HOST]
    topic = EVENTS_TOPIC
    auto_offset_reset = "earliest"


class Consumer:
    def __init__(self, config: ConsumerConfig):
        self.client = KafkaConsumer(
            config.topic,
            bootstrap_servers=config.bootstrap_servers,
            auto_offset_reset=config.auto_offset_reset,
            # add more configs here if you'd like
        )
        self.topic = config.topic

    def consume(self):
        """Consume messages from a Redpanda topic"""
        try:
            for msg in self.client:
                print(f"Consumed record. key={msg.key}, value={msg.value}")
        except:
            print(f"Could not consume from topic: {self.topic}")
            raise


config = ConsumerConfig()
redpanda_consumer = Consumer(config)
redpanda_consumer.consume()
