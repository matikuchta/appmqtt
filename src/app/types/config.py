from typing import TypedDict
class Config(TypedDict):
    broker:str
    client_id:str
    save_path:str
    port:int
    keepalive:int
    topics:list[str]