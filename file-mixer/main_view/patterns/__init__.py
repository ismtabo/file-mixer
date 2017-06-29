from abc import ABC, abstractmethod

class Serializable(ABC):

    def __init__(self):
        super(Serializable, self).__init__()

    @abstractmethod
    def serialize(self):
        pass

    @staticmethod
    @abstractmethod
    def unserialize(marshall):
        pass
