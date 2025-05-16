import sys
import logging as log
import json
from app.types.person import Person
from app.types.config import Config
def loadPersons(config:Config)->tuple[list[Person], str]:
    try:
        path:str = config["save_path"]
        if len(sys.argv)>2:
            path = sys.argv[2]
            log.debug(f"save file opened: {path}")
        with open(path, "r") as file:
            persons:list[Person] = json.load(file)
            log.debug(f"file {path} loaded, persons: {persons}")
    except Exception as e:
        persons:list[Person]=[]
        print(f"file {path} not loaded: {e}")
    return persons, path
