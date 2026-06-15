# Ingest Streaming Data into Apache Pinot

**There is an article now**. [Yet another end-to-end streaming dashboarding example](https://dev.to/agileactors/yet-another-end-to-end-streaming-dashboarding-example-43dp)

## Preparation

Notice that the docker compose file deploys both Kafka and Pinot.

It is a minimally adpated example from [here](https://docs.pinot.apache.org/start-here/install/docker). We will use a python application to ingest wikipedia events and send them to kafka.

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
podman build -t pinot-advanced/python-streaming-ingest ./producer-app
```

and then, we run it

``` sh
podman run -it  --network=pinot-advanced pinot-advanced/python-streaming-ingest:latest
```

For convenience, a consumer app is provided as a debugging means [consumer-app](./consumer-app) 

``` sh
podman build -t pinot-advanced/python-kafka-consumer ./consumer-app
podman run -it  --network=pinot-advanced pinot-advanced/python-kafka-consumer:latest
```

Now, we can setup Pinot to create a streaming table for this stream

``` sh
podman run -it --network=pinot-advanced -v ./scripts/wikipedia_events_schema.json:/scripts/wikipedia_events_schema.json -v ./scripts/wikipedia_events_realtime_table_config.json:/scripts/wikipedia_events_realtime_table_config.json apachepinot/pinot:latest-25-ms-openjdk AddTable -schemaFile /scripts/wikipedia_events_schema.json -tableConfigFile /scripts/wikipedia_events_realtime_table_config.json -controllerHost pinot-controller -exec
```

## Changes if you like to use RedPanda

You can also use the corresponding RedPanda docker [compose file](./redpanda-docker-compose.yml)

It was adapted from [here]().

In streamer-app comment this line

```
conf = {'bootstrap.servers': 'kafka'}
```

and comment out this line

```
# conf = {'bootstrap.servers': 'redpanda-0,redpanda-1,redpanda-2'}
```

`consumer-app` needs a similar change. Change also the bootstrap from

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

A Panel dashboard, in the form of a Jupyter Notebook is provided. It is advised to create a virtual environment and install the [requirements.txt](panel-dashboard-app\requirements.txt) there. I execute the dashboard in VScodium using this virtual environment as a kernel. 

You can serve it, if you like, is as follows

```sh 
panel serve .\dashboard.ipynb
```

Feel free to study the notebook since it uses some advanced concepts from [Panel Streaming Dashoboards](https://panel.holoviz.org/tutorials/basic/build_streaming_dashboard.html)
