# MQTT personel menagement system operating on JSON objects
## Features
- add person
- modify person
- delete person
- get person
- get all persons
- get the number of persons on the list
- saving all data to a .json file

## Used Technology
- Python 3.10
- paho-mqtt

# Data storage
all persons can be stored in a .json file, an example file is provided. 
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
# Command Structure
the command is given in the topic of the message
the topic follows this pattern: ```app/[...]/[...]/request```
and the needed data in the message content as JSON
the app will respond with a topic ```app/[...]/[...]/response``` and message containing the requested data, if any
#### Message
```
{
'data':
  {
  'status': 'success',
  'contain': {}
  },
'info':
  {
'ts': 1746695904
  }
}
```
the status will be either success or error
contain will store the requested data, if any
ts will store the timestamp of the response
# Reqests and responses
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
```
{
'data':
  {
  'status': 'success',
  'contain': {}
  },
'info':
  {
'ts': 1746695904
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
```
{
'data':
  {
  'status': 'success',
  'contain': {}
  },
'info':
  {
'ts': 1746695904
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
```
{
'data':
  {
  'status': 'success',
  'contain': {}
  },
'info':
  {
'ts': 1746695904
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
"pesel": "12345678901",

}
```
the pesel number is used to identify the person
### Response
#### Topic
```
app/person/get/response
```
#### Message
```
{
'data':
  {
    'status': 'success',
    'contain':
{'{"imie": "jan", "nazwisko": "kowalski", "pesel": "12345678901", "stanowisko": "kierownik", "data_zatrudnienia": "2025-05-08T09:50:01.444494", "data_urodzenia": "2025-05-08T09:50:01.444494", "data_utworzenia": "2025-05-08T09:50:01.444494", "data_modyfikacji": "2025-05-08T09:50:01.444494"}'}
  },
'info':
  {
  'ts': 1746690667
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
```
{
data':
  {'status': 'success',
  'contain': {'[{"imie": "jan", "nazwisko": "kowalski", "pesel": "12345678901", "stanowisko": "kierownik", "data_zatrudnienia": "2025-05-08T10:09:44.421447", "data_urodzenia": "2025-05-08T10:09:44.421447", "data_utworzenia": "2025-05-08T10:09:44.421447", "data_modyfikacji": "2025-05-08T10:09:44.421447"}]'}},
'info':
  {
  'ts': 1746695934
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
```
{'data': {'status': 'success', 'contain': {'count': '0'}}, 'info': {'ts': 1746690946}}
```







