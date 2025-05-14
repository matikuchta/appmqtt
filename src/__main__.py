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
from app.types.updatepersondata import UpdatePersonData
from app.types.getdelpersondata import GetDelPersonData


log.basicConfig(level=log.DEBUG)

def handleExit(signal: int, frame: Any)->None:
    log.info("The app has been terminated successfully")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handleExit)
    if len(sys.argv)<2:
        with open("config.json", "r") as f:
            config:Config = json.load(f)
    else:
        with open(sys.argv[1], "r") as f:
            config:Config = json.load(f)
            print(f"config opened from file: {sys.argv[1]}")

    client = MQTTClient(config)

    try:
        path = config["save_path"]
        with open(path, "r") as file:
            persons:list[Person] = json.load(file)
            print(f"file {path} loaded, persons: {persons}")
    except Exception as e:
        persons=[]
        print(f"file {path} not loaded: {e}")

    sub = PersonFasada(config, persons, "sub1")
    for topic in config.get("topics"):
        client.attach(sub, topic)
    client.connect()
    client.subscribe("app/+/+/request")
    client.client.loop_start()
    '''FLASK'''
    app = Flask(__name__)
    @app.route('/')
    def root():
        return "root"
    @app.get('/person')
    def get_person():
        pesel = request.args.get('pesel')
        data:GetDelPersonData = {'pesel': pesel}
        res = sub.GetPerson(data)
        log.debug(res)
        return jsonify(res)
    @app.get('/persons')
    def get_persons():
        res = sub.GetPersons()
        log.debug(res)
        return jsonify(res)
    @app.post('/person')
    def add_person():
        person:Person = {
            "imie" : request.args.get('imie'),
            "nazwisko" : request.args.get('nazwisko'),
            "pesel" : request.args.get('pesel'),
            "stanowisko" : request.args.get('stanowisko'),
            "data_urodzenia" : request.args.get('data_urodzenia'),
            "data_zatrudnienia" : request.args.get('data_zatrudnienia')
        }
        sub.AddPerson(json.dumps(person))
        sub.SaveData()
        return jsonify({})
    @app.delete('/person')
    def del_person():
        pesel = request.args.get('pesel')
        data:GetDelPersonData = {'pesel': pesel}
        sub.RemovePerson(json.dumps(data))
        sub.SaveData()
        return jsonify({})
    @app.patch('/person')
    def patch_person():
        person_data:Person = {}
        if request.args.get('imie'):
            person_data["imie"] = request.args.get('imie')
        if request.args.get('nazwisko'):
            person_data["nazwisko"] = request.args.get('nazwisko')
        if request.args.get('stanowisko'):
            person_data["stanowisko"] = request.args.get('stanowisko')
        if request.args.get('data_urodzenia'):
            person_data["data_urodzenia"] = request.args.get('data_urodzenia')
        if request.args.get('data_zatrudnienia'):
            person_data["data_zatrudnienia"] = request.args.get('data_zatrudnienia')
        print(json.dumps(person_data))
        data:UpdatePersonData = {
            "pesel" : request.args.get('pesel'),
            "to_update" : person_data
        }
        sub.ModifyPerson(json.dumps(data))
        sub.SaveData()
        return jsonify({})
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    '''FLASK'''
