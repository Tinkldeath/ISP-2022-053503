from abc import ABC, abstractmethod


class Converter(ABC):
    @abstractmethod
    def split_iterable(self, s: str) -> str:
        pass

    @abstractmethod
    def split_dict(self, s: str) -> str:
        pass