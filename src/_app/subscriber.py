from _app.publisher import IPublisher
from abc import ABC, abstractmethod

class ISubscriber(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def handleMessage(self, message:str, publisher:IPublisher)-> None:
        pass