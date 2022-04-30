from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def dump(self, obj: object, fp: str):  # сериализует Python объект в файл
        pass

    @abstractmethod
    def dumps(self, obj: object) -> str:  # сериализует Python объект в строку
        pass

    @abstractmethod
    def load(self, fp: str) -> object:  # десериализует Python объект из файла
        pass

    @abstractmethod
    def loads(self, s: str) -> object:  # десериализует Python объект из строки
        pass
