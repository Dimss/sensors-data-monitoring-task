# Sensor Data Monitoring and Alerting System

## Project structure 

* Sensors metrics streamer and validator includes the following 
  * [Main Service](main_service) -> Main orchestrator implementation 
  * [Sensors](sensors) -> The sensor metrics reader and metrics simulator
  * [Configuration](config) -> The configuration parsing logic and the `config.yml` file

* Alert manager 
  * [Alert Manager](alert_service) -> Redis PubSub listener and alerting to Slack chanel
 
* Redis PubSub client implementation 
  * [Redis Queue](queue_impl) -> Redis PubSub client and connection manager
 
* Application entry point
  * [Cli Interface](main.py) -> CLI implementation and OS signals handler

## Architecture schema
```

      |----|
      | S1 |--->|       |------------|                        |-------------|
      |----|    |       |            |                        |             |
                |------>|Orchestrator|----->Redis Pub/Sub---->|Alert Manager|-----> Slack Notification
      |----|    |       |            |                        |             |
      | S2 |--->|       |------------|                        |-------------|
      |----|
```

## Installation
* Docker & Docker compose
  * Install docker & docker compose 
  * run `docker-compose up --build`
  * for getting real Slack notification, update `compose.yaml` file and set `SLACK_CHANNEL` and `SLACK_TOKEN` to valid values   
 
* Run locally 
  * Install `python 3.11` version 
  * Install requirements `pip3 install -r requirements.txt`
  * Start local Redis instance
  * To start sensor connectors run `python3 main.py start sensor-connectors`
  * To start alerter run `python main.py start alerter`
  * If needed update `config.yml` under config `directory/` 