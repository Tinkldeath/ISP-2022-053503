import os.path
from Modules.lib.factory.serializer_factory import Serializer
from Modules.lib.abstract.converter import Converter


class JSONStringConverter(Converter):

    def __init__(self):
        pass

    def split_dict(self, s: str) -> str:
        open_braces = 0
        close_braces = 0
        res_string = ""
        for ch in s:
            if ch == '{':
                open_braces += 1
            elif ch == '}':
                close_braces += 1
                if open_braces == close_braces:
                    res_string += ch
                    return res_string
                else:
                    res_string += ch
                    continue
            res_string += ch

    def split_iterable(self, s: str) -> str:
        open_braces = 0
        close_braces = 0
        res_string = ""
        for ch in s:
            if ch == '[':
                open_braces += 1
            elif ch == ']':
                close_braces += 1
                if open_braces == close_braces:
                    res_string += ch
                    return res_string
                else:
                    res_string += ch
                    continue
            res_string += ch


class JSONSerializer(Serializer):

    __converter = JSONStringConverter()

    def dump(self, obj: object, fp: str):  # сериализует Python объект в файл
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
        if os.path.exists(fp):
            with open(fp, 'r') as file:
                s = file.read()
                s = s.replace("\n", "")
                s = s.replace(" ", "")
            return self.__load_typed(s)
        else:
            print("File is not exist")

    def loads(self, s) -> object:  # десериализует Python объект из строки
        s = s.replace("\n", "")
        s = s.replace(" ", "")
        return self.__load_typed(s)

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
            return self.__serialize_iterable(value)
        if t is bool:
            if value is True:
                return "true"
            else:
                return "false"
        if value is None:
            return "null"

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

    def __load_typed(self, s: str) -> object:
        if s[0] == '{' and s.__contains__(':'):
            value = self.__converter.split_dict(s)
            return self.__load_dict(value)
        elif s[0] == '[':
            value = self.__converter.split_iterable(s)
            return self.__load_list(value)
        else:
            if s.isdigit():
                if s.__contains__('.'):
                    return float(s)
                else:
                    return int(s)
            elif s == "true":
                return True
            elif s == "false":
                return False
            elif s == "null":
                return None
            else:
                return s

    def __load_dict(self, s: str) -> dict:
        d = dict()
        i = 1
        s = s.replace('"', "")
        n = len(s)
        key = ""
        value = ""
        while i < n:
            if s[i] == ':':
                j = i + 1
                if j > n:
                    return d
                elif s[j] == '{':
                    while j < n:
                        value += s[j]
                        j += 1
                    value = self.__converter.split_dict(value)
                elif s[j] == '[':
                    while j < n:
                        value += s[j]
                        j += 1
                    value = self.__converter.split_iterable(value)

                else:
                    while j < n and s[j] != ',' and s[j] != '}':
                        value += s[j]
                        j += 1
                i += len(value) + 2
                d[key] = self.__load_typed(value)
                key = ""
                value = ""
            else:
                key += s[i]
                i += 1
        return d

    def __load_list(self, s: str) -> list:
        l = list()
        i = 1
        n = len(s)
        value = ""
        while i < n:
            if s[i] == '{':
                j = i
                while j < n:
                    value += s[j]
                    j += 1
                value = self.__converter.split_dict(value)
            elif s[i] == '[':
                j = i
                while j < n:
                    value += s[j]
                    j += 1
                value = self.__converter.split_iterable(value)
            else:
                j = i
                while j < n and s[j] != ',':
                    value += s[j]
                    j += 1
            i += len(value)
            l.append(self.__load_typed(value))
            value = ""
            i += 1
        return l
