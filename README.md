# MQTT personel menagement system operating on JSON objects <!-- omit in toc -->
# this readme is not up to date: please check the documentation in the docs folder <!--omit in toc-->
# Table of contents <!-- omit in toc -->
- [this readme is not up to date: please check the documentation in the docs folder ](#this-readme-is-not-up-to-date-please-check-the-documentation-in-the-docs-folder-)
- [Features](#features)
- [Used Technology](#used-technology)
- [Config](#config)
- [Person Structure](#person-structure)
- [MQTT Command Structure](#mqtt-command-structure)
- [MQTT Reqests and responses](#mqtt-reqests-and-responses)
  - [Adding a person](#adding-a-person)
  - [Modifying a person](#modifying-a-person)
  - [Deleting a person](#deleting-a-person)
  - [Geting the data of a person](#geting-the-data-of-a-person)
  - [Geting the data of all persons](#geting-the-data-of-all-persons)
  - [Geting the count of all persons](#geting-the-count-of-all-persons)
- [API requests and responses](#api-requests-and-responses)
  - [View all API requests](#view-all-api-requests)
    - [Request - GET](#request---get)
  - [Get a list of all persons](#get-a-list-of-all-persons)
  - [Get the number of persons on the list](#get-the-number-of-persons-on-the-list)
    - [Request - GET](#request---get-1)
    - [Response](#response)
  - [Get a person by pesel number](#get-a-person-by-pesel-number)
  - [Add a person](#add-a-person)
  - [Update a person](#update-a-person)
  - [Delete a person](#delete-a-person)

# Features
- add person
- modify person
- delete person
- get person
- get all persons
- get the number of persons on the list
- saving all data to a .json file
- loading a custom config.json file
- api support

# Used Technology
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
Message
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
### Request <!-- omit in toc -->
Topic
```
app/person/add/request
```
Message
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
### Response <!-- omit in toc -->
Topic
```
app/person/add/response
```
Message
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
### Request <!-- omit in toc -->
Topic
```
app/person/update/request
```
Message

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
### Response <!-- omit in toc -->
Topic
```
app/person/update/response
```
Message
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
### Request <!-- omit in toc -->
Topic
```
app/person/del/request
```
Message

``` JSON
{
"pesel": "12345678901"

}
```
the pesel number is used to identify the person that is about to be deleted
### Response <!-- omit in toc -->
Topic
```
app/person/del/response
```
Message
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
### Request <!-- omit in toc -->
Topic
```
app/person/get/request
```
Message

``` JSON
{
"pesel": "12345678901"

}
```
the pesel number is used to identify the person
### Response <!-- omit in toc -->
Topic
```
app/person/get/response
```
Message
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
### Request <!-- omit in toc -->
Topic
```
app/persons/get/request
```
Message
the message is empty
### Response <!-- omit in toc -->
Topic
```
app/persons/get/response
```
Message
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
### Request <!-- omit in toc -->
Topic
```
app/persons/count/request
```
Message
the message is empty
### Response <!-- omit in toc -->
Topic
```
app/persons/count/response
```
Message
```JSON
{"data": {"status": "success", "contain": {"count": "0"}}, "info": {"ts": 1746690946}}
```

# API requests and responses
## View all API requests
### Request - GET
```
http://127.0.0.1:5000/help
```
## Get a list of all persons
### Request - GET <!-- omit in toc -->
```
http://127.0.0.1:5000/persons
```
### Response <!-- omit in toc -->
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
## Get the number of persons on the list
### Request - GET
```
http://127.0.0.1:5000/persons/count
```
### Response
```JSON
7
```
## Get a person by pesel number
### Request - GET <!-- omit in toc -->
```
http://127.0.0.1:5000/person?pesel=12345678905
```
### Resposnse <!-- omit in toc -->
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
### Request- POST <!-- omit in toc --> 
```
http://127.0.0.1:5000/person?pesel=12345678905&imie=Adam&nazwisko=Nowak&stanowisko=mechanik&data_urodzenia=2000-02-02&data_zatrudnienia=2024-01-01
```
add all of the data
### Resposnse <!-- omit in toc -->
```JSON
{}
```
## Update a person
### Request - PATCH <!-- omit in toc -->
```
http://127.0.0.1:5000/person?pesel=12345678905&imie=Jan&nazwisko=Nowak&stanowisko=elektryk
```
you need to add the pesel number and only the data you want to update. the pesel won't be updated
### Resposnse <!-- omit in toc -->
```JSON
{}
```
## Delete a person
### Request  - DELETE <!-- omit in toc -->
```
http://127.0.0.1:5000/person?pesel=12345678905
```
only the pesel is needed
### Resposnse <!-- omit in toc -->
```JSON
{}
```








