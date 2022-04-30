from abc import ABC, abstractmethod


class Serializable(ABC):
    @abstractmethod
    def to_serializable(self) -> dict:
        pass
