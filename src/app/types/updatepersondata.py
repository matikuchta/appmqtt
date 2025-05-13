from typing import TypedDict
from app.types.person import Person
class UpdatePersonData(TypedDict):
    pesel:str
    to_update:dict[Person]