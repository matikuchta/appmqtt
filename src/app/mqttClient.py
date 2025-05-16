from datetime import datetime
import json
from paho.mqtt.client import Client
import logging as log

from app.publisher import IPublisher
from app.subscriber import ISubscriber
from app.personFasada import PersonFasada
from app.types.config import Config
from app.types.mqttconfig import MQTTConfig

class MQTTClient(IPublisher):
    subscribers:dict[str, list[ISubscriber]]={}
    def __init__(self,config:Config) -> None:
        self.config:MQTTConfig = config["mqtt"]
        self.client:Client = Client(client_id=self.config["client_id"])
        self.broker:str = self.config["broker"]
        self.port:int = self.config["port"]
        self.keepalive:int = self.config["keepalive"]
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    def on_connect(self, broker:str, port:int, keepalive:int, reasonCode:str) -> None:
        log.debug(f"Connected with reason code:{reasonCode}")
    def on_disconnect(self, reasonCode:str) -> None:
        log.debug("Disconnected with reason code:", reasonCode)
    def on_message(self, client, userdata, msg)-> None:
        subs=self.subscribers.get(msg.topic, [])
        for sub in subs:
            log.debug(f"message handled by: {sub.name}")
            sub.handleMessage(msg, self)
           

    def connect(self) -> None:
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            log.debug(f"Connected to broker {self.broker} on port {self.port}")
        except Exception as e:
            print(f"Connect error: {e}")
    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
    def subscribe(self, topic:str) -> None:
        log.debug(f"Broker subscribed to topic '{topic}'")
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
    def attachAll(self, sub:PersonFasada, topics:list[str]):
        for topic in topics:
            self.attach(sub, topic)
