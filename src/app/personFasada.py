from datetime import datetime
import json
from paho.mqtt.client import Client
import time
from typing import TYPE_CHECKING, List, TypedDict

from app.publisher import IPublisher
from app.subscriber import ISubscriber
from app.types.person import Person
import logging as log
import re
# if TYPE_CHECKING:

class PersonFasada(ISubscriber):
    def __init__(self, path:str="", persons:List[Person]=[], name:str="subscriber") -> None:
        self.name=name
        self.path = path
        self.persons=persons
    def ValidateData(self, data:dict) -> bool:
        try:
            if re.search("^[A-Z]{,1}[a-z]{2,}$", data["imie"]) and re.search("^[A-Z]{,1}[a-z]{1,}$", data["nazwisko"]) and re.search("^[0-9]{11}$", data["pesel"]):
                #required_keys = {"data_urodzenia", "data_zatrudnienia", "stanowisko"}
                #if required_keys.issubset(data) and len(data) == 6:
                return True
            else: return False
        except:
            return False
    def AddPerson(self, data:dict) -> bool:
        data=json.loads(data)
        data["data_utworzenia"] = datetime.now().isoformat()
        data["data_modyfikacji"] = datetime.now().isoformat()
        ok = True
        for person in self.persons:
            if person["pesel"]==data["pesel"]:
                ok = False
        if ok and self.ValidateData(data):
            self.persons.append(data)
            return True
        else:
            return False

    def ModifyPerson(self, data:dict) ->bool:
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                for key, value in data["to_update"].items():
                    if key == "data_utworzenia" or key not in person.keys():
                        return False
                    # print(f"{key} {value}\n")
                    else:
                        person[key]=value
                        person["data_modyfikacji"] = datetime.now().isoformat()
                return True

    def RemovePerson(self, data:dict) -> bool:
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                self.persons.remove(person)
                return True
        return False
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
        print(f"recieved message {msg.payload.decode()} on topic: {msg.topic}")
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
                    if not self.AddPerson(mes):
                        raise Exception("Encountered problems with adding data")


                case "app/person/update/request":
                    if not self.ModifyPerson(mes):
                        raise Exception("Encountered problems with updating data")

                case "app/person/del/request":
                    if not self.RemovePerson(mes):
                        raise Exception("Encountered problems with deleting data")


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
            try:
                if self.path != "":
                    with open(self.path, "w") as file:
                        json.dump(self.persons, file, indent=2)
            except Exception as e:
                print(f"data not saved to file")


