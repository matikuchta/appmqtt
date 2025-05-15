from flask import Flask, request, jsonify, send_file
import logging as log
import json

from app.types.person import Person
from app.types.config import Config
from app.personFasada import PersonFasada
from app.types.updatepersondata import UpdatePersonData
from app.types.getdelpersondata import GetDelPersonData
class API:
    def __init__(self, app:Flask, sub:PersonFasada):
        self.sub:PersonFasada = sub
        app.add_url_rule('/', 'root', self.root)
        app.add_url_rule('/help', 'help', self.help)
        app.add_url_rule('/person', 'get_person', self.get_person, methods=['GET'])
        app.add_url_rule('/persons', 'get_persons', self.get_persons, methods=['GET'])
        app.add_url_rule('/persons/count', 'get_persons_count', self.get_persons_count, methods=['GET'])
        app.add_url_rule('/person', 'add_person', self.add_person, methods=['POST'])
        app.add_url_rule('/person', 'del_person', self.del_person, methods=['DELETE'])
        app.add_url_rule('/person', 'patch_person', self.patch_person, methods=['PATCH'])
    def root(self)->str:
        return "<h1>Persons API</h1><p>use /help to view commands</p>"
    def help(self)->str:
        return send_file("help.html")
    def get_person(self)->json:
        pesel:str = request.args.get('pesel')
        data:GetDelPersonData = {'pesel': pesel}
        res = self.sub.GetPerson(data)
        log.debug(res)
        return jsonify(res)
    def get_persons(self)->json:
        res:json = self.sub.GetPersons()
        log.debug(res)
        return jsonify(res)
    def get_persons_count(self)->json:
        res:json = self.sub.GetPersonsCount()
        return jsonify(res)
    def add_person(self)->json:
        person:Person = {
            "imie" : request.args.get('imie'),
            "nazwisko" : request.args.get('nazwisko'),
            "pesel" : request.args.get('pesel'),
            "stanowisko" : request.args.get('stanowisko'),
            "data_urodzenia" : request.args.get('data_urodzenia'),
            "data_zatrudnienia" : request.args.get('data_zatrudnienia')
        }
        self.sub.AddPerson(json.dumps(person))
        self.sub.SaveData()
        return jsonify({})
    def del_person(self)->json:
        pesel:str = request.args.get('pesel')
        data:GetDelPersonData = {'pesel': pesel}
        self.sub.RemovePerson(json.dumps(data))
        self.sub.SaveData()
        return jsonify({})
    def patch_person(self)->json:
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
        self.sub.ModifyPerson(json.dumps(data))
        self.sub.SaveData()
        return jsonify({})
    
