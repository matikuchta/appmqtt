# MQTT personel menagement system operating on JSON objects
## Features
- add person
- modify person
- delete person
- get person
- get all persons
- get the number of persons on the list
- saving all data to a .json file
- api support

## Used Technology
- Python 3.10
- libraries:
  - paho-mqtt
  - requests
  - flask

# Config
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
You can specify the path to your configuration file as an argument like this: ```python3 ./src/__main__.py ./src/config.json```, otherwise, the default config is used
# Person Structure

this is an example of a JSON object containing all of the stored information about a single person
``` JSON
{
  "imie": "jan",
  "nazwisko": "kowalski",
  "pesel": "12345678901",
  "stanowisko": "kierownik",
  "data_zatrudnienia": "2025-05-08T10:09:44.421447",
  "data_urodzenia": "2025-05-08T10:09:44.421447",
  "data_utworzenia": "2025-05-08T10:09:44.421447",
  "data_modyfikacji": "2025-05-08T10:09:44.421447"
}
```
# MQTT Command Structure
the command is given in the topic of the message
the topic follows this pattern: ```app/[...]/[...]/request```
and the needed data in the message content as JSON
the app will respond with a topic ```app/[...]/[...]/response``` and message containing the requested data, if any
#### Message
```JSON
{
"data":
  {
  "status": "success",
  "contain": {}
  },
"info":
  {
"ts": 1746695904
  }
}
```
the status will be either success or error
contain will store the requested data, if any
ts will store the timestamp of the response
# MQTT Reqests and responses
## Adding a person
### Request
#### Topic
```
app/person/add/request
```
#### Message
``` JSON
{
  "imie": "name",
  "nazwisko": "surname",
  "pesel": "12345678901",
  "stanowisko": "job",
  "data_zatrudnienia": "date_of_employment",
  "data_urodzenia": "date_of_birth",
}
```
pesel must be a 11 digit number, name and surname can contain only letters
### Response
#### Topic
```
app/person/add/response
```
#### Message
```JSON
{
"data":
  {
  "status": "success",
  "contain": {}
  },
"info":
  {
"ts": 1746695904
  }
}
```
this request does not return any data in contain
## Modifying a person
### Request
#### Topic
```
app/person/update/request
```
#### Message

``` JSON
{
"pesel": "12345678901",
"to_update":{
  "imie": "new_name"
}
}
```
the pesel number is used to identify the person
to_update contains the fields that are to be updated as keys and new values as values
### Response
#### Topic
```
app/person/update/response
```
#### Message
```JSON
{
"data":
  {
  "status": "success",
  "contain": {}
  },
"info":
  {
"ts": 1746695904
  }
}
```
this request does not return any data in contain
## Deleting a person
### Request
#### Topic
```
app/person/del/request
```
#### Message

``` JSON
{
"pesel": "12345678901"

}
```
the pesel number is used to identify the person that is about to be deleted
### Response
#### Topic
```
app/person/del/response
```
#### Message
```JSON
{
"data":
  {
  "status": "success",
  "contain": {}
  },
"info":
  {
"ts": 1746695904
  }
}
```
this request does not return any data in contain
## Geting the data of a person
### Request
#### Topic
```
app/person/get/request
```
#### Message

``` JSON
{
"pesel": "12345678901"

}
```
the pesel number is used to identify the person
### Response
#### Topic
```
app/person/get/response
```
#### Message
```JSON
{
"data":
  {
    "status": "success",
    "contain":
{"imie": "jan", "nazwisko": "kowalski", "pesel": "12345678901", "stanowisko": "kierownik", "data_zatrudnienia": "2025-05-08T09:50:01.444494", "data_urodzenia": "2025-05-08T09:50:01.444494", "data_utworzenia": "2025-05-08T09:50:01.444494", "data_modyfikacji": "2025-05-08T09:50:01.444494"}
  },
"info":
  {
  "ts": 1746690667
  }
}
```
## Geting the data of all persons
### Request
#### Topic
```
app/persons/get/request
```
#### Message
the message is empty
### Response
#### Topic
```
app/persons/get/response
```
#### Message
```JSON
{
"data":
  {"status": "success",
  "contain": [{"imie": "jan", "nazwisko": "kowalski", "pesel": "12345678901", "stanowisko": "kierownik", "data_zatrudnienia": "2025-05-08T10:09:44.421447", "data_urodzenia": "2025-05-08T10:09:44.421447", "data_utworzenia": "2025-05-08T10:09:44.421447", "data_modyfikacji": "2025-05-08T10:09:44.421447"}]},
"info":
  {
  "ts": 1746695934
  }
}
```
## Geting the count of all persons
### Request
#### Topic
```
app/persons/count/request
```
#### Message
the message is empty
### Response
#### Topic
```
app/persons/count/response
```
#### Message
```JSON
{"data": {"status": "success", "contain": {"count": "0"}}, "info": {"ts": 1746690946}}
```

# API Requests
## Get all persons
### Request - GET
```
http://127.0.0.1:5000/persons
```
### Response
```JSON
[
    {
        "data_modyfikacji": "2025-05-12T10:32:33.854899",
        "data_urodzenia": "2025-05-08T10:09:44.421447",
        "data_utworzenia": "2025-05-08T10:09:44.421447",
        "data_zatrudnienia": "2025-05-08T10:09:44.421447",
        "imie": "adam",
        "nazwisko": "nowak",
        "pesel": "12345678901",
        "stanowisko": "kierownik"
    },
    {
        "data_modyfikacji": "2025-05-08T10:09:44.421447",
        "data_urodzenia": "2025-05-08T10:09:44.421447",
        "data_utworzenia": "2025-05-08T10:09:44.421447",
        "data_zatrudnienia": "2025-05-08T10:09:44.421447",
        "imie": "jan",
        "nazwisko": "kowalski",
        "pesel": "12345678900",
        "stanowisko": "kierownik"
    }
]
```
## Get a single person
### Request - GET
```
http://127.0.0.1:5000/person?pesel=12345678905
```
### Resposnse
```JSON
{
    "data_modyfikacji": "2025-05-14T11:55:46.738037",
    "data_urodzenia": "2000-02-02",
    "data_utworzenia": "2025-05-14T11:55:46.738037",
    "data_zatrudnienia": "2024-01-01",
    "imie": "Adam",
    "nazwisko": "Nowak",
    "pesel": "12345678905",
    "stanowisko": "mechanik"
}
```
## Add a person
### Request - POST
```
http://127.0.0.1:5000/person?pesel=12345678905&imie=Adam&nazwisko=Nowak&stanowisko=mechanik&data_urodzenia=2000-02-02&data_zatrudnienia=2024-01-01
```
### Resposnse
```JSON
{}
```
## Update a person
### Request - patch
```
http://127.0.0.1:5000/person?pesel=12345678905&imie=Jan&nazwisko=Nowak&stanowisko=elektryk
```
### Resposnse
```JSON
{}
```
## Delete a person
### Request - DELETE
```
http://127.0.0.1:5000/person?pesel=12345678905
```
### Resposnse
```JSON
{}
```








