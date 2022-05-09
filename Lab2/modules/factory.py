from modules.abstract_serializer import Serializer
from modules.serializers.json_serializer import JsonSerializer

SERIALIZERS = {
    'json': JsonSerializer(),
    'yaml': None,
    'toml': None
}


class SerializerFactory:
    @staticmethod
    def create_serializer(serializer_type: str):
        serializer = SERIALIZERS.get(serializer_type.lower(), None)
        if not serializer:
            raise ValueError(f'Format {serializer_type} is not supported')
        return serializer
