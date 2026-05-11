#see here https://dev.to/hantedyou_0106/building-a-kafka-wikimedia-producer-understanding-constructors-and-threading-1nmo

from confluent_kafka import Producer, admin
import datetime
import json
from requests_sse import EventSource

kafka_topic_name = "wikipedia-events"

# conf = {'bootstrap.servers': 'redpanda-0,redpanda-1,redpanda-2'}
conf = {'bootstrap.servers': 'kafka'}

kafka_admin = admin.AdminClient(conf)

kafka_admin.delete_topics([kafka_topic_name])
kafka_admin.create_topics([admin.NewTopic(kafka_topic_name, 1, 1)])

producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        ...
        # print("Message produced: %s" % (str(msg)))

events_processed = 0 

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
headers = {"User-Agent": "advanced_pinot_tutorial"}

with EventSource(url, headers=headers) as stream:
    for event in stream:
         if event.type == 'message':
            try:
                change = json.loads(event.data)
                change['ts'] = change['timestamp'] * 1000
                del change['timestamp']

                producer.poll(0)
                producer.produce(kafka_topic_name, key=change["meta"]["id"], value=json.dumps(change), callback=acked)

                events_processed += 1
                if events_processed == 100:
                    print(f"{str(datetime.datetime.now())} Flushing after {events_processed} events")
                    producer.flush()
                    events_processed = 0  
            except ValueError:
                pass