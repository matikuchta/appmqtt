from datetime import datetime
import json
from paho.mqtt.client import Client
import time
from app.personFasada import PersonFasada

class MQTTClient:
    pf=PersonFasada()
    subscribers = []
    def __init__(self, client_id, broker, port=1883, keepalive=60):
        self.client = Client(client_id=client_id)
        self.broker = broker
        self.port = port
        self.keepalive = keepalive
        # Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    def on_connect(self, client, userdata, flags, reasonCode):
        print("Connected with reason code:", reasonCode)
    def on_disconnect(self, client, userdata, flags, reasonCode):
        print("Disconnected with reason code:", reasonCode)
    def on_message(self, client, userdata, msg):
        print(f"RECIEVED\n---TOPIC---\n{msg.topic}\n---MESSAGE---\n{msg.payload.decode()}")
        mes = msg.payload.decode()
        #mes=mes["data"]
        #print(msg)
        res = {
            "data": {
                "status": "success",
                "contain":{}
                     },
            "info": {"ts": int(datetime.now().timestamp())}
        }
        top1:str=msg.topic
        top=top1.replace("request", "response")
        #print(top)
        try:
            match msg.topic:
                case "app/person/add/request":
                    self.pf.AddPerson(mes)

                case "app/person/update/request":
                    self.pf.ModifyPerson(mes)

                case "app/person/del/request":
                    self.pf.RemovePerson(mes)

                case "app/person/get/request":
                    print("response", self.pf.GetPerson(mes))
                    res["data"].update({"contain": {self.pf.GetPerson(mes)}})

                case "app/persons/get/request":
                    print("response", self.pf.GetPersons())
                    res["data"].update({"contain": {self.pf.GetPersons()}})

                case "app/persons/count/request":
                    print("response", self.pf.GetPersonsCount())
                    res["data"].update({"contain": {"count": self.pf.GetPersonsCount()}})

                case _:
                    pass

        except Exception as e:
            res["data"]["status"] = "error"
            print(f"Error handling topic {msg.topic}: {e}")
        finally:
            self.publish(str(top), str(res))
            #with open("persons.json", "w") as file:
                #file.write(json.dumps(self.pf.persons))


    def connect(self):
        try:
            self.client.connect(self.broker, self.port, self.keepalive)
            print("Connected to broker")
        except Exception as e:
            print(f"Connect error: {e}")
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
    def subscribe(self, topic):
        print(f"\nSubscribed to topic '{topic}'")
        self.client.subscribe(topic)
    def publish(self, topic, message):
        self.client.publish(topic, message)
        print(f"PUBLISHED\n---TOPIC---\n{topic}\n---MESSAGE---\n{message}\n")
