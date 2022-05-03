import os
from Modules.lib.abstract.serializer import Serializer
from Modules.lib.abstract.converter import Converter


class TomlStringConverter(Converter):
    def split_dict(self, s: str) -> str:
        pass

    def split_iterable(self, s: str) -> str:
        pass


class TomlSerializer(Serializer):

    __converter = TomlStringConverter()

    def dump(self, obj: object, fp: str):
        if os.path.exists(fp):
            file = open(fp, "w")
            file.write(self.__serialize_typed(type(obj), obj, ""))
            file.close()
            print(f'Object serialized to file {fp}')
        else:
            print("File is not exist")

    def dumps(self, obj: object) -> str:
        return self.__serialize_typed(obj)

    def load(self, fp: str) -> object:
        pass

    def loads(self, s: str) -> object:
        pass

    def __serialize_typed(self, t: type, value, key, level=0) -> str:
        if t is str:
            return f'"{value}"'
        if t is int or t is float:
            return f'{value}'
        if t is tuple or t is list or t is set:
            for el in value:
                if type(el) != dict:
                    return self.__serialize_default_iterable(value)
            return self.__serialize_iterable(value, key, level+1)
        if t is dict:
            return self.__serialize_dict(value, key, level+1)
        if t is bool:
            if value is True:
                return "true"
            else:
                return "false"
        return f'"null"'

    def __serialize_dict(self, item: dict, key, level=0) -> str:
        answer = ""
        if key != "":
            answer += (level * '[') + f'{key}' + (level*']') + '\n'
        for k, value in item.items():
            if type(value) is dict:
                if key != "":
                    kk = f'{key}.{k}'
                else:
                    kk = f'{k}'
                answer += f'{self.__serialize_typed(type(value), value, kk, level-1)}\n'
            elif type(value) is list or type(value) is set or type(value) is tuple:
                for el in value:
                    if type(el) != dict:
                        answer += f'{k} = {self.__serialize_typed(type(value), value, key, level)}\n'
                        break
                    else:
                        if key != "":
                            kk = f'{key}.{k}'
                        else:
                            kk = f'{k}'
                        if level > 1:
                            answer += f'{self.__serialize_typed(type(value), value, kk, level-1)}\n'
                        else:
                            answer += f'{self.__serialize_typed(type(value), value, kk, level)}\n'
                        break
            else:
                answer += f'{k} = {self.__serialize_typed(type(value), value, key,level)}\n'
        answer += '\n'
        return answer

    def __serialize_iterable(self, item, key, level=0) -> str:
        answer = ""
        if key != "":
            answer += (level * '[') + f'{key}' + (level*']') + '\n'
        for el in item:
            if type(el) is dict:
                if level > 1:
                    answer += f'{self.__serialize_typed(type(el), el, key, level-1)}\n'
                else:
                    answer += f'{self.__serialize_typed(type(el), el, key, level)}\n'
            elif type(el) is list or type(el) is set or type(el) is tuple:
                answer += f'{self.__serialize_typed(type(el), el, key, level)}\n'
            else:
                answer += f'{self.__serialize_typed(type(el), el, key, level)}, '
        new_answer = answer[:-2]
        return new_answer

    def __serialize_default_iterable(self, item) -> str:
        answer = '[ '
        for el in item:
            answer += f'{self.__serialize_typed(type(el), el, "")}, '
        new_answer = answer[:-2]
        new_answer += ' ]'
        return new_answer
