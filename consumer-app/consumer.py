# Purpose: Consumes all messages from Kafka topic for testing purposes
# Author:  Gary A. Stafford
# Date: 2022-08-29
# Instructions: Modify the configuration.ini file to meet your requirements.
#               Select the topic to view the messages from.

import json
from kafka import KafkaConsumer


def main():
    # choose any or all topics

    consumer = KafkaConsumer(
        "wikipedia-events",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        # bootstrap_servers='redpanda-0:9092'
        bootstrap_servers='kafka:9092'
    )

    for message in consumer:
        print(message.value)


if __name__ == "__main__":
    main()