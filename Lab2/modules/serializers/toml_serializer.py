import pytoml
import os
from modules.abstract_serializer import Serializer
from modules.converter import Converter


class TomlSerializer(Serializer):

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
        if type(converted) is not dict:
            return ""
        return pytoml.dumps(converted, sort_keys=True)

    def load(self, fp: str) -> object:
        if os.path.exists(fp):
            file = open(fp, "r")
            s = file.read()
            file.close()
            return self.loads(s)
        else:
            print(f'File {fp} not found')

    def loads(self, s: str) -> object:
        obj = pytoml.loads(s)
        return Converter.load(obj)
