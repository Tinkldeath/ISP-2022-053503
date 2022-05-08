import os
from Modules.lib.abstract.serializer import Serializer
from Modules.lib.abstract.converter import Converter
from Modules.lib.factory.typed_serializer import TypedSerializer


class TomlStringConverter(Converter):
    def split_dict(self, s: str) -> str:
        answer = ""
        array = s.split("\n")
        key = array[0]
        key = key.replace("[", "")
        key = key.replace("]", "")
        i = 1
        n = len(array)
        while i < n:
            if array[i].count("[") >= 1:
                if array[i].count(key) == 0 or array[i] == key:
                    break
            answer += array[i] + "\n"
            i += 1
        return answer

    def split_iterable(self, s: str) -> str:
        answer = ""
        array = s.split("\n")
        key = array[0]
        comp_key = array[0]
        comp_key = comp_key.replace("[", "")
        answer += array[0] + "\n"
        i = 1
        n = len(array)
        while i < n-2:
            if array[i] == key:
                i += 1
                while i < n - 2:
                    if array[i] == key:
                        break
                    else:
                        answer += array[i] + "\n"
                        i += 1
            else:
                break
        return answer


class TomlSerializer(Serializer):

    __converter = TomlStringConverter()

    def dump(self, obj: object, fp: str):
        if os.path.exists(fp):
            file = open(fp, "w")
            file.write(self.__serialize_dict(obj, "", 1))
            file.close()
            print(f'Object serialized to file {fp}')
        else:
            print("File is not exist")

    def dumps(self, obj: object) -> str:
        return self.__serialize_typed(obj)

    def load(self, fp: str) -> object:
        if os.path.exists(fp):
            with open(fp, 'r') as file:
                s = file.read()
            return self.__load_full(s)
        else:
            print("File is not exist")

    def loads(self, s: str) -> object:
        pass

    def __serialize_typed(self, t: type, value, key, level=0) -> str:
        if t is str:
            return f'"{value}"'
        elif t is int or t is float:
            return f'{value}'
        elif t is tuple or t is list or t is set:
            for el in value:
                if type(el) != dict:
                    return self.__serialize_default_iterable(value)
            return self.__serialize_iterable(value, key, level+1)
        elif t is dict:
            return self.__serialize_dict(value, key, level+1)
        elif t is bool:
            if value is True:
                return "true"
            else:
                return "false"
        elif hasattr(value, '__call__'):
            return self.__serialize_dict(TypedSerializer.serialize_func(value), "")
        return f'"null"'

    def __serialize_dict(self, item: dict, key, level=0) -> str:
        answer = ""
        last_key = list(item.keys())[-1]
        last_item = item[last_key]
        if key != "" and level > 1:
            answer += (level * '[') + f'{key}' + (level*']') + '\n'
        for k, value in item.items():
            if type(value) is dict:
                if key != "":
                    kk = f'{key}.{k}'
                else:
                    kk = f'{k}'
                if level > 1:
                    answer += (level * ' ') + f'{self.__serialize_typed(type(value), value, kk, level - 1)}'
                else:
                    answer += f'{self.__serialize_typed(type(value), value, kk, level - 1)}'
            elif type(value) is list or type(value) is set or type(value) is tuple:
                for el in value:
                    if type(el) != dict:
                        answer += (level * ' ') + f'{k} = {self.__serialize_typed(type(value), value, key, level)}'
                        break
                    else:
                        if key != "":
                            kk = f'{key}.{k}'
                        else:
                            kk = f'{k}'
                        if level > 1:
                            answer += (level * ' ') + f'{self.__serialize_typed(type(value), value, kk, level-1)}\n'
                        else:
                            answer += f'{self.__serialize_typed(type(value), value, kk, level-1)}\n'
                        break
            else:
                if level > 1:
                    answer += (level * ' ') + f'{k} = {self.__serialize_typed(type(value), value, key, level)}\n'
                else:
                    answer += f'{k} = {self.__serialize_typed(type(value), value, key, level)}\n'
        if last_item is dict or list:
            answer += "\n"
        return answer

    def __serialize_iterable(self, item, key, level=0) -> str:
        answer = ""
        last_item = item[-1]
        if key != "":
            answer += (level * '[') + f'{key}' + (level*']') + '\n'
        for el in item:
            if type(el) is dict:
                if level > 1:
                    answer += (level * ' ') + f'{self.__serialize_typed(type(el), el, key, level-1)}'
                else:
                    answer += (level * ' ') + f'{self.__serialize_typed(type(el), el, key, level)}'
            elif type(el) is list or type(el) is set or type(el) is tuple:
                answer += (level * ' ') + f'{self.__serialize_typed(type(el), el, key, level)}'
            else:
                answer += (level * ' ') + f'{self.__serialize_typed(type(el), el, key, level)}, '
        new_answer = answer[:-2]
        if last_item is dict or list:
            new_answer += "\n"
        return new_answer

    def __serialize_default_iterable(self, item) -> str:
        answer = '[ '
        for el in item:
            answer += f'{self.__serialize_typed(type(el), el, "")}, '
        new_answer = answer[:-2]
        new_answer += ' ]'
        return new_answer

    def __load_typed(self, s: str) -> object:
        s = s.replace('"', "")
        s = s.replace(" ", "")
        if s.count("[") == 1:
            return self.__load_default_array(s)
        elif s == "true":
            return True
        elif s == "false":
            return False
        elif s == "null":
            return None
        elif s.isdigit():
            return int(s)
        elif s.count('.') > 0:
            try:
                return float(s)
            except ValueError:
                return s
        return s

    def __load_full(self, s: str) -> dict:
        d = dict()
        a = s.split("\n")
        for el in a:
            if el == "":
                a.remove(el)
        i = 0
        n = len(a)
        while i < n-1:
            if a[i].count('[') >= 1:
                k = a[i]
                k = k.replace("]", "")
                k = k.replace("[", "")
                k = k.replace(".", "")
                k = k.replace(" ", "")

                nk = a[i + 1]
                nk = nk.replace("]", "")
                nk = nk.replace("[", "")
                nk = nk.replace(".", "")
                nk = nk.replace(" ", "")

                if k == nk:
                    level = spacing_count(a[i + 1])
                    i += 1
                    value = ""
                    while spacing_count(a[i]) >= level and i < n - 1:
                        value += a[i] + "\n"
                        i += 1
                    d[k] = self.__load_table_array(value, k)
                else:
                    i += 1
                    level = spacing_count(a[i])
                    value = ""
                    while spacing_count(a[i]) >= level and i < n - 1:
                        value += a[i] + "\n"
                        i += 1
                    d[k] = self.__load_table(value, nk)
            else:
                try:
                    k, value = a[i].split('=')
                    k = k.replace(" ", "")
                    d[k] = self.__load_typed(value)
                except ValueError:
                    break
            i += 1
        return d

    def __load_table(self, s: str, key: str) -> dict:
        d = dict()
        a = s.split("\n")
        i = 0
        n = len(a)
        while i < n-1:
            if a[i].count('[') >= 1 and a[i].count(key) > 0:
                k = a[i]
                k = k.replace("]", "")
                k = k.replace("[", "")
                k = k.replace(key, "")
                k = k.replace(".", "")
                k = k.replace(" ", "")

                nk = a[i+1]
                nk = nk.replace("]", "")
                nk = nk.replace("[", "")
                nk = nk.replace(key, "")
                nk = nk.replace(".", "")
                nk = nk.replace(" ", "")

                array_key = a[i+1]

                if k == nk:
                    level = spacing_count(a[i+1])
                    i += 1
                    value = ""
                    while spacing_count(a[i]) >= level and i < n-1:
                        value += a[i] + "\n"
                        i += 1
                    d[k] = self.__load_table_array(value, array_key)
                    i += 1
                else:
                    i += 1
                    level = spacing_count(a[i])
                    value = ""
                    while spacing_count(a[i]) >= level and i < n - 1 and a[i].count("[") == 0:
                        value += a[i] + "\n"
                        i += 1
                    d[k] = self.__load_table(value, k)
            else:
                try:
                    k, value = a[i].split('=')
                    k = k.replace(" ", "")
                    d[k] = self.__load_typed(value)
                    i += 1
                except ValueError:
                    break
        return d

    def __load_table_array(self, s: str, key: str) -> list:
        l = list()
        a = s.split("\n")
        i = 0
        n = len(a)
        while i < n-1:
            if a[i].count("[") > 0 and a[i].count(key) > 0:
                level = spacing_count(a[i + 1])
                i += 1
                value = ""
                while spacing_count(a[i]) >= level and i < n-1 and a[i] != key:
                    value += a[i] + "\n"
                    i += 1
                l.append(self.__load_table(value, key))
        return l

    def __load_default_array(self, s: str) -> list:
        l = list()
        a = s.split(",")
        for el in a:
            l.append(self.__load_typed(el))
        return l


def spacing_count(s: str):
    i = 0
    n = len(s)
    count = 0
    while i < n:
        if s[i] == ' ':
            count += 1
        else:
            break
        i += 1
    return count