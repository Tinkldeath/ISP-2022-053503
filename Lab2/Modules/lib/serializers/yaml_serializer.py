import os
from Modules.lib.abstract.serializer import Serializer
from Modules.lib.abstract.converter import Converter


class YamlStringConverter(Converter):

    def split_dict(self, s: str) -> str:
        pass

    def split_iterable(self, s: str) -> str:
        pass


class YamlSerializer(Serializer):

    __converter = YamlStringConverter()

    def dump(self, obj: object, fp: str):
        if os.path.exists(fp):
            file = open(fp, "w")
            file.write(self.__serialize_typed(type(obj), obj))
            file.close()
            print(f'Object serialized to file {fp}')
        else:
            print("File is not exist")

    def dumps(self, obj: object) -> str:
        return self.__serialize_typed(type(obj), obj)

    def load(self, fp: str) -> object:
        pass

    def loads(self, s: str) -> object:
        pass

    def __serialize_typed(self, t: type, value: object, level: int = 0) -> str:
        if t is str:
            return f'"{value}"'
        if t is int or t is float:
            return f'{value}'
        if t is tuple or t is list or t is set:
            return self.__serialize_iterable(value, level+1)
        if t is dict:
            return self.__serialize_dict(value, level+1)
        if t is bool:
            if value is True:
                return "true"
            else:
                return "false"
        if value is None:
            return "null"

    def __serialize_iterable(self, item, level: int = 0) -> str:
        answer = "\n"
        answer += level*'\t' + "---\n"
        for element in item:
            answer += level*'\t' + f'-\t{self.__serialize_typed(type(element), element, level+1)}\n'
        return answer

    def __serialize_dict(self, item: dict, level: int = 0):
        answer = "\n"
        answer += level*'\t' + "---\n"
        for key, value in item.items():
            answer += level*'\t' + f'\t{key}:\t{self.__serialize_typed(type(value), value, level+1)}\n'
        return answer
