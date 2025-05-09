from datetime import datetime
import json
from paho.mqtt.client import Client
import time
from app.mqttClient import MQTTClient
from app.personFasada import PersonFasada


client = MQTTClient(client_id="myclient", broker="127.0.0.1")
#jan = CreatePerson("jan", "kowalski", "12345678901", "kierownik", datetime.now().isoformat(), datetime.now().isoformat())
#adam = CreatePerson("adam", "kowalski", "12345678901", "kierownik", datetime.now().isoformat(), datetime.now().isoformat())

client.connect()
client.subscribe('app/+/+/request')
#client.publish("app/person/add/request", json.dumps(jan))
client.client.loop_forever()
