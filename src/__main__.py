from paho.mqtt.client import Client
import sys
import signal
import json
import logging as log
from typing import Any
from flask import Flask, request, jsonify


from app.mqttClient import MQTTClient
from app.personFasada import PersonFasada
from app.types.person import Person
from app.types.config import Config
from app.loadconfig import LoadConfig
from app.loadPersons import loadPersons
from app.types.updatepersondata import UpdatePersonData
from app.types.getdelpersondata import GetDelPersonData
from app.api import API


log.basicConfig(level=log.DEBUG)

def handleExit(signal: int, frame: Any)->None:
    if sub.SaveData():
        log.debug(f"data saved successfully to save file: {path}")
    log.info("The app has been terminated successfully")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handleExit)

    config:Config = LoadConfig()

    client:MQTTClient = MQTTClient(config)

    persons, path = loadPersons(config)
    
    sub:PersonFasada = PersonFasada(config, persons, path, "sub1")
    client.attachAll(sub, config["mqtt"].get("topics"))
    client.connect()
    client.subscribe("app/+/+/request")
    client.client.loop_start()
    app = Flask(__name__)
    api = API(app, sub)
    app.run(host=config["flask"]["adress"], port=config["flask"]["port"], debug=config["flask"]["debug"], use_reloader=False)

