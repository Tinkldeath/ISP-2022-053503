from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def dump(self, obj: object, fp: str):
        pass

    @abstractmethod
    def dumps(self, obj: object) -> str:
        pass

    @abstractmethod
    def load(self, fp: str) -> object:
        pass

    @abstractmethod
    def loads(self, s: str) -> object:
        pass
