from datetime import datetime
import json
from paho.mqtt.client import Client
import logging as log

from app.publisher import IPublisher
from app.subscriber import ISubscriber
from app.personFasada import PersonFasada
from app.types.config import Config

class MQTTClient(IPublisher):
    pf=PersonFasada("src/persons.json")
    subscribers:dict[str, list[ISubscriber]]={}
    def __init__(self,config:Config) -> None:
        self.config:Config = config
        self.client:Client = Client(client_id=config["client_id"])
        self.broker:str = config["broker"]
        self.port:int = config["port"]
        self.keepalive:int = config["keepalive"]
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    def on_connect(self, broker:str, port:int, keepalive:int, reasonCode:str) -> None:
        print("Connected with reason code:", reasonCode)
    def on_disconnect(self, reasonCode:str) -> None:
        print("Disconnected with reason code:", reasonCode)
    def on_message(self, client, userdata, msg)-> None:
        subs=self.subscribers.get(msg.topic, [])
        for sub in subs:
            log.debug(f"message handled by: {sub.name}")
            sub.handleMessage(msg, self)
           

    def connect(self) -> None:
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            print(f"Connected to broker {self.broker} on port {self.port}")
        except Exception as e:
            print(f"Connect error: {e}")
    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
    def subscribe(self, topic:str) -> None:
        log.debug(f"\n Broker subscribed to topic '{topic}'")
        self.client.subscribe(topic)
    def publish(self, topic:str, message:str) -> None:
        if topic in self.subscribers:
            for sub in self.subscribers[topic]:
                sub.handleMessage(message, self)
        #log.debug(f"PUBLISHED\n---TOPIC---\n{topic}\n---MESSAGE---\n{message}\n")
        self.client.publish(topic, message)
    def attach(self, subscriber:ISubscriber, topic:str)->None:
        if topic not in self.subscribers:
            self.subscribers[topic] =[]
        self.subscribers[topic].append(subscriber)
        log.debug(f"subscriber {subscriber.name} attached to topic {topic}")
