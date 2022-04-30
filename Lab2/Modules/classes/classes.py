from abc import ABC
from Modules.lib.abstract.serializable import Serializable


class Person(Serializable, ABC):
    def __init__(self, full_name: str, email: str, phone: str, age: int):
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
        serializable['type'] = "Person"
        serializable['full_name'] = self.__full_name
        serializable['email'] = self.__email
        serializable['phone'] = self.__phone
        serializable['age'] = self.__age
        return serializable


class Company(Serializable, ABC):
    __name: str = "default_name"
    __director: Person = None
    __employee: [Person] = []
    __is_legal: bool = True

    def __init__(self, name: str, director: Person, employee: [Person], legal: bool):
        self.__name = name
        self.__director = director
        self.__employee = employee
        self.__is_legal = legal

    def to_serializable(self) -> dict:
        s = dict()
        s['type'] = "Company"
        s['name'] = self.__name
        s['director'] = self.__director.to_serializable()
        emp = list()
        for employee in self.__employee:
            emp.append(employee.to_serializable())
        s['employee'] = emp
        s['is_legal'] = self.__is_legal
        return s
