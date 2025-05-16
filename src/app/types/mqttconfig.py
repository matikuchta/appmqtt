from typing import TypedDict
class MQTTConfig(TypedDict):
    broker:str
    port:int
    client_id:str
    keepalive:int
    topics:list[str]