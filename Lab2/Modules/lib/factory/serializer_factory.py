from Modules.lib.abstract.serializer import Serializer
from Modules.lib.serializers.json_serializer import JSONSerializer
from Modules.lib.serializers.yaml_serializer import YamlSerializer
from Modules.lib.serializers.toml_serializer import TomlSerializer

SERIALIZERS = {
    "json": JSONSerializer(),
    "yaml": YamlSerializer(),
    "toml": TomlSerializer()
}


class SerializerFactory(object):
    @staticmethod
    def create_serializer(serializer_type: str) -> Serializer:
        serializer = SERIALIZERS.get(serializer_type.lower(), None)
        if not serializer:
            raise ValueError(f'Format {serializer_type} is not supported')
        return serializer
