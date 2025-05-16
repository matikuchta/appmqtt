from typing import TypedDict
from app.types.mqttconfig import MQTTConfig
from app.types.flaskconfig import FlaskConfig
class Config(TypedDict):
    save_path:str
    mqtt:MQTTConfig
    flask:FlaskConfig
    