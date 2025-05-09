from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


# Zapobiega to przed zapętlonym importem pomiędzy subscriber a publisher
if TYPE_CHECKING:
    from app.publisher import IPublisher

class ISubscriber(ABC):
    @abstractmethod
    def handleMessage(self, message:str, publisher:IPublisher)-> None:
        pass