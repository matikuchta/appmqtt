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
## persons.json
- the persons.json file stores a json list of person objects
- You can specify the path to your data storage file as a second argument like this: ```python3 ./src/__main__.py ./"src/config.json" "src/persons.json" ```, otherwise, the default config is used