import inspect
from modules.parsers.json_parser import JsonParser
from types import CodeType


class JsonSerializer:

    @staticmethod
    def _dumps(obj, step='', new_step=''):
        if obj is None:
            return "null"
        elif obj is True:
            return "true"
        elif obj is False:
            return "false"
        elif obj is float("Inf"):
            return "Infinity"
        elif obj is float("-Inf"):
            return "-Infinity"
        elif obj is float("NaN"):
            return "NaN"
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, bytes):
            return "\"" + str(list(bytearray(obj))) + "\""
        elif isinstance(obj, str):
            return "\"" + obj.replace('\\', '\\\\').replace('\"', '\\\"') + "\""
        elif isinstance(obj, (set, tuple)):
            return JsonSerializer.dumps_list(list(obj), step, new_step)
        elif isinstance(obj, list):
            return JsonSerializer.dumps_list(obj, step, new_step)
        elif isinstance(obj, dict):
            return JsonSerializer.dumps_dict(obj, step, new_step)
        elif inspect.isfunction(obj):
            res = JsonSerializer.dumps_dict(JsonParser.function_to_dict(obj), step, new_step)
            JsonSerializer.func_found = {}
            return res
        elif isinstance(obj, staticmethod):
            res = JsonSerializer.dumps_dict(JsonParser.static_method_to_dict(obj), step, new_step)
            JsonSerializer.func_found = {}
            return res
        elif isinstance(obj, classmethod):
            res = JsonSerializer.dumps_dict(JsonParser.class_method_to_dict(obj), step, new_step)
            JsonSerializer.func_found = {}
            return res
        elif inspect.ismodule(obj):
            return JsonSerializer.dumps_dict(JsonParser.module_to_dict(obj), step, new_step)
        elif inspect.isclass(obj):
            return JsonSerializer.dumps_dict(JsonParser.class_to_dict(obj), step, new_step)
        elif JsonParser.is_instance(obj):
            return JsonSerializer.dumps_dict(JsonParser.object_to_dict(obj), step, new_step)
        elif isinstance(obj, CodeType):
            return JsonSerializer.dumps_dict(JsonParser.code_to_dict(obj), step, new_step)
        else:
            raise TypeError()

    @staticmethod
    def dumps_list(obj, step="", new_step=""):
        if not len(obj):
            return "[]"
        new_step = "\n" + new_step
        res = "[" + new_step
        for i in range(len(obj) - 1):
            res += step + JsonSerializer._dumps(obj[i], step, new_step.replace('\n', '') + step) + "," + new_step
        res += step + JsonSerializer._dumps(obj[-1], step, new_step.replace('\n', '') + step) + new_step + "]"
        return res

    @staticmethod
    def dumps_dict(obj, step="", new_step=""):
        if not len(obj):
            return "{}"
        if JsonParser.sort:
            obj = dict(sorted(obj.items()))
        new_step = "\n" + new_step
        res = "{" + new_step
        keys = list(obj)
        for i in keys[:-1]:
            res += step + '"' + str(i) + '"' + ": " + JsonSerializer._dumps(obj[i], step,
                                                                            new_step.replace('\n',
                                                                                             '') + step) + "," + new_step
        res += step + '"' + str(keys[-1]) + '"' + ": " + JsonSerializer._dumps(obj[keys[-1]], step,
                                                                               new_step.replace('\n',
                                                                                                '') + step) + new_step + "}"
        return res

    @staticmethod
    def dump(obj, fp, sort_keys=False, indent=None):
        try:
            with open(fp, 'w') as file:
                file.write(JsonSerializer.dumps(obj, sort_keys, indent))
        except FileNotFoundError:
            raise FileNotFoundError("file doesn't exist")

    @staticmethod
    def dumps(obj, sort_keys=False, indent=None):
        JsonParser.func_found = {}
        JsonParser.sort = sort_keys
        if isinstance(indent, int) and indent > 0:
            step = " " * indent
            res = JsonSerializer._dumps(obj, step)
            if indent < 1:
                res = res.replace("\n", "")
        else:
            res = JsonSerializer._dumps(obj).replace("\n", "")
        return res

    @staticmethod
    def load(fp):
        try:
            with open(fp, 'r') as file:
                data = file.read()
        except FileNotFoundError:
            raise FileNotFoundError("file doesn't exist")
        return JsonSerializer.loads(data)

    @staticmethod
    def loads(string):
        index = 0
        try:
            while string[index] == ' ' or string[index] == '\n':
                index += 1
        except IndexError:
            pass

        if string[index] == '"':
            obj, index = JsonParser.parse_string(string, index + 1)
        elif string[index].isdigit() or (string[index] == '-' and string[index + 1].isdigit()):
            obj, index = JsonParser.parse_digit(string, index)
        elif string[index] == '{':
            obj, index = JsonParser.parse_dict(string, index + 1)
        elif string[index] == '[':
            obj, index = JsonParser.parse_array(string, index + 1)
        elif string[index] == 'n' and string[index:index + 4] == 'null':
            obj = None
            index += 4
        elif string[index] == 't' and string[index:index + 4] == 'true':
            obj = True
            index += 4
        elif string[index] == 'f' and string[index:index + 5] == 'false':
            obj = False
            index += 5
        elif string[index] == 'N' and string[index:index + 3] == 'NaN':
            obj = False
            index += 3
        elif string[index] == 'I' and string[index:index + 8] == 'Infinity':
            obj = float('Infinity')
            index += 8
        elif string[index] == '-' and string[index:index + 9] == '-Infinity':
            obj = float('-Infinity')
            index += 9
        else:
            raise StopIteration(index)

        try:
            while True:
                if string[index] != ' ' and string[index] != '\n':
                    raise StopIteration(index)
                index += 1
        except IndexError:
            pass

        return obj
