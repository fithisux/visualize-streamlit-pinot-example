# Ingest Streaming Data into Apache Pinot

## Preparation

Notice that the docker compose file deploys both Kafka and Pinot.

It is a minimally adpated example from [here](https://docs.pinot.apache.org/start-here/install/docker)
We will use a python application to ingest wikipedia events and send them to kafka.

Nothing needs to change.

We also use a `.env` file so as to configure our Pinot example.

To this end copy the default provided file

```
cp env.default .env
```

, change what needs to be changed, and start the application with Podman

```
podman compose up -d
```

To stop it later, just run

```
podman compose down -v
```

## Generate data

For this, we need to run a node app to consume the wikipedia event stream and write it to Kafaka
First, we will build the (streamer app)[./streamer app] Docker image:

``` sh
podman build -t pinot-advanced/python-streaming-ingest ./streamer-app

```

and then, we run it

```
podman run -it  --network=pinot-advanced pinot-advanced/python-streaming-ingest:latest
```

For convenience, a consumer app is provided as a debugging means [consumer-app](./consumer-app) 
that can be run on your PC, so as to verify that Kafka is getting the events. 
Please use a virtual environment.

You can also achieve similar effect with an (IntelliJ plugin)[https://plugins.jetbrains.com/plugin/21704-confluent].

Now, we can setup Pinot to create a streaming table for this stream

```
podman run -it --network=pinot-advanced -v ./scripts/wikipedia_events_schema.json:/scripts/wikipedia_events_schema.json -v ./scripts/wikipedia_events_realtime_table_config.json:/scripts/wikipedia_events_realtime_table_config.json apachepinot/pinot:latest-25-ms-openjdk AddTable -schemaFile /scripts/wikipedia_events_schema.json -tableConfigFile /scripts/wikipedia_events_realtime_table_config.json -controllerHost pinot-controller -exec
```

## Changes if you like to use RedPanda

You can also use the corresponding RedPanda docker [compose file](./redpanda-docker-compose.yml)

In streamer-app comment this line

```
conf = {'bootstrap.servers': 'kafka'}
```

and comment out this line

```
# conf = {'bootstrap.servers': 'redpanda-0,redpanda-1,redpanda-2'}
```

Change also the bootstrap from

```
kafka:9092
```

to

```
redpanda-0:9092
```

in [this file](./scripts/wikipedia_events_realtime_table_config.json).

## Launching the UI

Once that's run, you can navigate the Pinot UI - [http://localhost:9000](http://localhost:9000)

- It takes a few minutes for Pinot to start
- Make sure that the wikievents table is created by navigating to  [http://localhost:9000/#/query](http://localhost:9000/#/query)

Feel free to query it.

The [original document](https://github.com/startreedata/learn/tree/main/pinot-advanced/04-stream-ingestion) proposes to follow this link for validation

the wikipedia events table is pupulated by navigating to: [http://localhost:9000/#/query?query=select+*+from+wikievents+limit+10&tracing=false&useMSE=false](http://localhost:9000/#/query?query=select+*+from+wikievents+limit+10&tracing=false&useMSE=false)

## Dashboarding

A streamlit dashboarding app is provided based on older code presented [here](https://github.com/pinot-contrib/pinot-docs/blob/latest/tutorials/getting-started/streamlit.md) with slight modifications.

Feel free to study it and run it in a virtual environment.
