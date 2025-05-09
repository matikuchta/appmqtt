from abc import ABC, abstractmethod
from src._app.subscriber import ISubscriber as ISubscriber
class IPublisher(ABC):
    @abstractmethod
    def __init__(self)->None:
        pass
    @abstractmethod
    def attach(self, subscriber:ISubscriber, topic:str)->None:
        pass