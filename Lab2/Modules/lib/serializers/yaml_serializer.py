import os
from Modules.lib.abstract.serializer import Serializer
from Modules.lib.abstract.converter import Converter
from Modules.lib.factory.typed_serializer import TypedSerializer


class YamlStringConverter(Converter):

    def split_dict(self, s: str) -> str:
        array = s.split(' ')
        for el in array:
            if el == '' or el == "":
                array.remove(el)
        top_level = 1
        bot_level = 0
        answer = ""
        i = 1
        n = len(array)
        while i < n:
            if array[i] == "---":
                top_level += 1
            elif array[i] == "...":
                bot_level += 1
                if bot_level == top_level:
                    break
            answer += array[i] + ' '
            i += 1
        return answer

    def split_iterable(self, s: str) -> str:
        array = s.split(' ')
        for el in array:
            if el == '' or el == "":
                array.remove(el)
        top_level = 1
        bot_level = 0
        answer = ""
        i = 1
        n = len(array)
        while i < n:
            if array[i] == "---":
                top_level += 1
            elif array[i] == "...":
                bot_level += 1
                if bot_level == top_level:
                    break
            answer += array[i] + ' '
            i += 1
        return answer


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
        if os.path.exists(fp):
            with open(fp, 'r') as file:
                s = file.read()
                s = s.replace("\n", " ")
                s = s.replace("'", "")
                s = s.replace("\t", "")
            return self.__load_typed(s)
        else:
            print("File is not exist")

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
        elif hasattr(value, '__call__'):
            return self.__serialize_typed(type(TypedSerializer.serialize_func(value)), TypedSerializer.serialize_func(value))
        return "null"

    def __serialize_iterable(self, item, level: int = 0) -> str:
        answer = "\n"
        answer += level*'\t' + "---\n"
        for element in item:
            answer += level*'\t' + f'- {self.__serialize_typed(type(element), element, level+1)}\n'
        answer += level*'\t' + "..."
        return answer

    def __serialize_dict(self, item: dict, level: int = 0):
        answer = "\n"
        answer += level*'\t' + "---\n"
        for key, value in item.items():
            answer += level*'\t' + f'\t{key}: {self.__serialize_typed(type(value), value, level+1)}\n'
        answer += level*'\t' + "..."
        return answer

    def __load_typed(self, s: str) -> object:
        s = s.replace('"', "")
        if len(s) > 6:
            if s[1] == '-' and s[5] != '-':
                return self.__load_dict(self.__converter.split_dict(s))
            elif s.count("-") > 0:
                return self.__load_list(self.__converter.split_iterable(s))
        elif s == "null":
            return None
        elif s == "true":
            return True
        elif s == "false":
            return False
        elif s.isdigit():
            return int(s)
        elif s.count('.') > 0:
            try:
                return float(s)
            except ValueError:
                return s
        return s

    def __load_dict(self, s: str) -> dict:
        array = s.split(' ')
        for el in array:
            if el == '' or el == "":
                array.remove(el)
        d = dict()
        i = 0
        n = len(array)
        while i < n-1:
            if array[i+1] == "---" and array[i+2] == "-":
                j = i+1
                s = ""
                while j < n:
                    s += array[j] + ' '
                    j += 1
                key = array[i].replace(':', "")
                value = self.__converter.split_iterable(s)
                d[key] = self.__load_list(value)
                i += len(value.split(' ')) + 2
            elif array[i+1] == "---":
                j = i+1
                s = ""
                while j < n:
                    s += array[j] + ' '
                    j += 1
                key = array[i].replace(':', "")
                value = self.__converter.split_dict(s)
                d[key] = self.__load_dict(value)
                i += (len(value.split(' '))) + 2
            else:
                key = array[i].replace(":", "")
                value = array[i+1]
                d[key] = self.__load_typed(value)
                i += 2
        return d

    def __load_list(self, s: str) -> list:
        array = s.split(' ')
        for el in array:
            if el == '' or el == "":
                array.remove(el)
        l = list()
        i = 0
        n = len(array)
        while i < n-2:
            if array[i] == '-' and array[i+1] == "---" and array[i+2] != "-":
                j = i + 1
                s = ""
                while j < n:
                    s += array[j] + ' '
                    j += 1
                value = self.__converter.split_dict(s)
                l.append(self.__load_dict(value))
                i += (len(value.split(' '))) + 2
            elif array[i] == "-" and array[i+1] == "---" and array[i+2] == "-":
                j = i + 1
                s = ""
                while j < n:
                    s += array[j] + ' '
                    j += 1
                value = self.__converter.split_iterable(s)
                l.append(self.__load_list(value))
                i += (len(value.split(' '))) + 2
            elif array[i] == "-":
                j = i+1
                value = ""
                count = 1
                while j < n and array[j] != "-" and array[j] != "---" and array[j] != "...":
                    value += array[j]
                    j += 1
                    count += 1
                l.append(self.__load_typed(value))
                i += count
        return l
