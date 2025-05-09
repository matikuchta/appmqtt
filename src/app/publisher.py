from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from app.subscriber import ISubscriber

class IPublisher(ABC):
    @abstractmethod
    def attach(self, subscriber:ISubscriber, topic:str)->None:
        pass