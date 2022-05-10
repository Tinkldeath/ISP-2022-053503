import os
from io import StringIO

from yaml import safe_dump, safe_load
from modules.abstract_serializer import Serializer
from modules.converter import Converter


class YamlSerializer(Serializer):
    def dump(self, obj: object, fp: str):
        s = self.dumps(obj)
        if os.path.exists(fp):
            file = open(fp, "w")
            file.write(s)
            file.close()
        else:
            print(f'File {fp} not found')

    def dumps(self, obj: object) -> str:
        converted = Converter.convert(obj)
        return safe_dump(converted)

    def load(self, fp: str) -> object:
        if os.path.exists(fp):
            with open(fp, "r") as file:
                obj = safe_load(file)
            return Converter.load(obj)
        else:
            print(f'File {fp} not found')

    def loads(self, s: str) -> object:
        str_stream = StringIO(s)
        obj = safe_load(str_stream)
        return Converter.load(obj)
