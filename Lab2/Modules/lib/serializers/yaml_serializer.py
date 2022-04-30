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
        pass

    def dumps(self, obj: object) -> str:
        pass

    def load(self, fp: str) -> object:
        pass

    def loads(self, s: str) -> object:
        pass
    