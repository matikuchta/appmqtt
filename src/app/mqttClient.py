from datetime import datetime
import json
from paho.mqtt.client import Client
import time
from app.personFasada import PersonFasada
from app.publisher import IPublisher
from app.subscriber import ISubscriber

class MQTTClient(IPublisher):
    pf=PersonFasada()
    subscribers:dict[str, list[ISubscriber]]={}
    def __init__(self, client_id:str, broker:str, port:int=1883, keepalive:int=60) -> None:
        self.client = Client(client_id=client_id)
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    def on_connect(self, broker:str, port:int, keepalive:int, reasonCode:str) -> None:
        print("Connected with reason code:", reasonCode)
    def on_disconnect(self, reasonCode:str) -> None:
        print("Disconnected with reason code:", reasonCode)
    def on_message(self, client, userdata, msg)-> None:
        subs=self.subscribers[msg.topic]
        for sub in subs:
            sub.handleMessage(msg, self)

    def connect(self) -> None:
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            print("Connected to broker")
        except Exception as e:
            print(f"Connect error: {e}")
    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
    def subscribe(self, topic:str) -> None:
        print(f"\nSubscribed to topic '{topic}'")
        self.client.subscribe(topic)
    def publish(self, topic:str, message:str) -> None:
        self.client.publish(topic, message)
        print(f"PUBLISHED\n---TOPIC---\n{topic}\n---MESSAGE---\n{message}\n")
    def attach(self, subscriber:ISubscriber, topic:str)->None:
        if topic not in self.subscribers:
            self.subscribers[topic] =[]
        self.subscribers[topic].append(subscriber)
