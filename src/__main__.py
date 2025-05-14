from paho.mqtt.client import Client
import sys
import signal
import json
import logging as log
from typing import Any


from app.mqttClient import MQTTClient
from app.personFasada import PersonFasada
from app.types.person import Person
from app.types.config import Config
from app.types.updatepersondata import UpdatePersonData
from app.types.getdelpersondata import GetDelPersonData
from app.api import API
from flask import Flask, request, jsonify


log.basicConfig(level=log.DEBUG)

def handleExit(signal: int, frame: Any)->None:
    log.info("The app has been terminated successfully")
    sub.SaveData()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handleExit)
    if len(sys.argv)<2:
        with open("config.json", "r") as f:
            config:Config = json.load(f)
    else:
        with open(sys.argv[1], "r") as f:
            config:Config = json.load(f)
            print(f"config opened from file: {sys.argv[1]}")

    client = MQTTClient(config)

    try:
        path = config["save_path"]
        with open(path, "r") as file:
            persons:list[Person] = json.load(file)
            print(f"file {path} loaded, persons: {persons}")
    except Exception as e:
        persons=[]
        print(f"file {path} not loaded: {e}")

    sub = PersonFasada(config, persons, "sub1")
    for topic in config.get("topics"):
        client.attach(sub, topic)
    client.connect()
    client.subscribe("app/+/+/request")
    client.client.loop_start()
    app = Flask(__name__)
    api = API(app, sub)
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

