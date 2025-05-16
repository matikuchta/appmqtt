import json
import sys
import logging as log
from app.types.config import Config
def LoadConfig():
    if len(sys.argv)<2:
        #opening default config
        with open("config.json", "r") as f:
            config:Config = json.load(f)
    else:
        with open(sys.argv[1], "r") as f:
            config:Config = json.load(f)
            log.debug(f"config opened from file: {sys.argv[1]}")
    return config