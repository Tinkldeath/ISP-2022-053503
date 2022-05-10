from modules.abstract_serializer import Serializer
from modules.serializers.yaml_serializer import YamlSerializer
from modules.serializers.json_serializer import JsonSerializer
from modules.serializers.toml_serializer import TomlSerializer

SERIALIZERS = {
    'json': JsonSerializer(),
    'yaml': YamlSerializer(),
    'toml': TomlSerializer()
}


class SerializerFactory:
    @staticmethod
    def create_serializer(serializer_type: str) -> Serializer:
        serializer = SERIALIZERS.get(serializer_type.lower(), None)
        if not serializer:
            raise ValueError(f'Format {serializer_type} is not supported')
        return serializer
