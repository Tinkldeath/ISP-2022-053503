import os.path
from Modules.lib.factory.serializer_factory import Serializer, SerializerFactory


class JSONSerializerFactory(SerializerFactory):
    def create_serializer(self):
        return JSONSerializer()


class JSONSerializer(Serializer):

    def __init__(self):
        pass

    def dump(self, obj, fp):  # сериализует Python объект в файл
        if os.path.exists(fp):
            file = open(fp, "w")
            file.write(self.__serialize_typed(type(obj), obj))
            file.close()
            print(f'Object serialized to file {fp}')
        else:
            print("File is not exist")

    def dumps(self, obj) -> str:  # сериализует Python объект в строку
        return self.__serialize_typed(type(obj), obj)

    def load(self, fp) -> object:  # десериализует Python объект из файла
        return

    def loads(self, s) -> object:  # десериализует Python объект из строки
        return

    def __serialize_typed(self, t: type, value) -> str:
        if t is str:
            return f'"{value}"'
        if t is int or t is float:
            return f'{value}'
        if t is tuple or t is list:
            return self.__serialize_iterable(value)
        if t is dict:
            return self.__serialize_dict(value)
        if t is set:
            return self.__serialize_set(value)
        if t is bool:
            if value is True:
                return "true"
            else:
                return "false"
        if t is None:
            return "null"

    def __serialize_set(self, s: set):
        answer = str()
        answer += "{ "
        for item in s:
            answer += self.__serialize_typed(type(item), item) + ", "
        new_answer = answer[:-2]
        new_answer += " }"
        return new_answer

    def __serialize_dict(self, d: dict) -> str:
        answer = str()
        answer += "{\n"
        for key, value in d.items():
            answer += f'"{key}": '
            t = type(value)
            answer += self.__serialize_typed(t, value) + ",\n"
        new_answer = answer[:-2]
        new_answer += "\n}"
        return new_answer

    def __serialize_iterable(self, item) -> str:
        answer = str()
        answer += "[ "
        for element in item:
            answer += self.__serialize_typed(type(element), element) + ", "
        new_answer = answer[:-2]
        new_answer += " ]"
        return new_answer
