from datetime import datetime
import json
from paho.mqtt.client import Client
import time
from typing import TYPE_CHECKING

from app.publisher import IPublisher
from app.subscriber import ISubscriber
import logging as log
# if TYPE_CHECKING:

class PersonFasada(ISubscriber):
    persons = []
    def __init__(self) -> None:
        with open("C:/Users/kuchta_m/appmqtt/persons.json", "r") as file:
            self.persons = json.load(file)
    def ValidateData(self, data:dict) -> bool:
        try:
            for x in data:
                if len(x)<3:
                    return False
            if len(data["pesel"])!=11:
                return False
            return True
        except:
            return False
    def AddPerson(self, data:dict) -> None:
        data=json.loads(data)
        ok = True
        for person in self.persons:
            if person["pesel"]==data["pesel"]:
                ok = False
        if ok and self.ValidateData(data):
            self.persons.append(data)

    def ModifyPerson(self, data:dict) -> None:
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                for key, value in data["to_update"].items():
                    print(f"{key} {value}\n")
                    person[key]=value
                person["data_modyfikacji"] = datetime.now().isoformat()

    def RemovePerson(self, data:dict) -> None:
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                self.persons.remove(person)
    def GetPerson(self, data:dict) -> json:
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                return json.dumps(person)
    def GetPersons(self) -> json:
        return json.dumps(self.persons)
    def GetPersonsCount(self) -> json:
        return json.dumps(len(self.persons))
    def handleMessage(self, msg:object, publisher:IPublisher) -> None:
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
                    self.AddPerson(mes)

                case "app/person/update/request":
                    self.ModifyPerson(mes)

                case "app/person/del/request":
                    self.RemovePerson(mes)

                case "app/person/get/request":
                    #print("response", self.GetPerson(mes))
                    res["data"]["contain"]=self.GetPerson(mes)

                case "app/persons/get/request":
                    #print("response", self.GetPersons())
                    res["data"]["contain"]=self.GetPersons()

                case "app/persons/count/request":
                    #print("response", self.GetPersonsCount())
                    res["data"]["contain"].update({"count": self.GetPersonsCount()})

                case _:
                    pass

        except Exception as e:
            res["data"]["status"] = "error"
            print(f"Error handling topic {msg.topic}: {e}")
        finally:
            log.debug(f"published {res} to topic {top}")
            publisher.publish(str(top), json.dumps(res))

            with open("C:/Users/kuchta_m/appmqtt/persons.json", "w") as file:
                json.dump(self.persons, file, indent=2)


