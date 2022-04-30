from abc import ABC
from Modules.serializable_type.serializable_type import Serializable


class Person(Serializable, ABC):
    def __init__(self, full_name: str, email: str, phone: str, age: str):
        self.__full_name = full_name
        self.__email = email
        self.__phone = phone
        self.__age = age

    __full_name: str = "default_name"
    __email: str = "default_email@gmail.com"
    __phone: str = "88005553535"
    __age: int = 18

    def to_serializable(self) -> dict:
        serializable = dict()
        serializable['type'] = """Person"""
        serializable['full_name'] = self.__full_name
        serializable['email'] = self.__email
        serializable['phone'] = self.__phone
        serializable['age'] = self.__age
        return serializable
