from paho.mqtt.client import Client
import sys
import time
import signal
import logging as log
from typing import Any
from app.mqttClient import MQTTClient
from app.personFasada import PersonFasada

log.basicConfig(level=log.DEBUG)

def handleExit(signal: int, frame: Any)->None:
    log.info("The app has been terminated successfully")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handleExit)
    
    client = MQTTClient(client_id="myclient", broker="127.0.0.1")
    #jan = CreatePerson("jan", "kowalski", "12345678901", "kierownik", datetime.now().isoformat(), datetime.now().isoformat())
    #adam = CreatePerson("adam", "kowalski", "12345678901", "kierownik", datetime.now().isoformat(), datetime.now().isoformat())
    sub = PersonFasada()
    client.attach(sub, "app/person/add/request")
    client.attach(sub, "app/person/del/request")
    client.attach(sub, "app/person/update/request")
    client.attach(sub, "app/person/get/request")
    client.attach(sub, "app/persons/get/request")
    client.attach(sub, "app/persons/count/request")

    client.connect()
    client.subscribe("app/+/+/request")
    #client.publish("app/person/add/request", json.dumps(jan))
    client.client.loop_forever()