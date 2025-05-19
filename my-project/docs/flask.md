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