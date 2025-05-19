## Config
``` JSON
{
    "broker":"127.0.0.1",
    "client_id":"myclient",
    "save_path":"src/persons.json",
    "port": 1883,
    "keepalive":60,
    "topics": [
    "app/person/add/request",
    "app/person/del/request",
    "app/person/update/request",
    "app/person/get/request",
    "app/persons/get/request",
    "app/persons/count/request"
]}
```
You can specify the path to your configuration file as an argument like this: ```python3 ./src/__main__.py "./src/config.json"```, otherwise, the default config is used