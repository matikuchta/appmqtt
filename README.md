# MQTT personel menagement system operating on JSON objects
## Features
- add person
- modify person
- delete person
- get person
- get all persons
- get the number of persons on the list

## Used Technology
- Python 3.10
- paho-mqtt

## Person Structure

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
## Commands
the command is given in the topic of the message
the topic follows this pattern: ```app/[...]/[...]/request```
and the needed data in the message content
the app will respond with a topic ```app/[...]/[...]/request```

### Creating a person
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
  "data_utworzenia": "date_of_creation",
  "data_modyfikacji": "date_of_modification"
}
```

### Modifying a person

### Deleting a person

### 






