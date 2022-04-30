from abc import ABC, abstractmethod


class SerializerFactory(ABC):
    @abstractmethod
    def create_serializer(self):
        pass


class Serializer(ABC):
    @abstractmethod
    def dump(obj, fp):  # сериализует Python объект в файл
        pass

    @abstractmethod
    def dumps(obj) -> str:  # сериализует Python объект в строку
        pass

    @abstractmethod
    def load(fp) -> object:  # десериализует Python объект из файла
        pass

    @abstractmethod
    def loads(s) -> object :  # десериализует Python объект из строки
        pass
