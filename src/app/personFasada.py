from datetime import datetime
import json
from paho.mqtt.client import Client
import time

class PersonFasada:
    persons = []
    def __init__(self):
        self.persons=[]
        #with open("persons.json", "r") as file:
           # self.persons = json.load(file)
    def ValidateData(self, data):
        try:
            for x in data:
                if len(x)<3:
                    return False
            if len(data["pesel"])!=11:
                return False
            return True
        except:
            return False
    def AddPerson(self, data):
        data=json.loads(data)
        ok = True
        for person in self.persons:
            if person["pesel"]==data["pesel"]:
                ok = False
        if ok and self.ValidateData(data):
            self.persons.append(data)

    def ModifyPerson(self, data):
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                for key, value in data["to_update"].items():
                    print(f"{key} {value}\n")
                    person[key]=value
                person.data_modyfikacji = datetime.now().isoformat()

    def RemovePerson(self, data):
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                self.persons.remove(person)
    def GetPerson(self, data):
        data=json.loads(data)
        for person in self.persons:
            if person["pesel"] == data["pesel"]:
                return json.dumps(person)
    def GetPersons(self):
        return json.dumps(self.persons)
    def GetPersonsCount(self):
        return json.dumps(len(self.persons))

