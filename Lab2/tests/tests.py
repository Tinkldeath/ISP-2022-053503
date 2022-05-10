import unittest
from modules.factory import SerializerFactory
from modules.converter import Converter
from tests_data import *


class TestClass(unittest.TestCase):
    def __init__(self, method):
        super().__init__(method)
        self.json = SerializerFactory.create_serializer("json")
        self.toml = SerializerFactory.create_serializer("toml")
        self.yaml = SerializerFactory.create_serializer("yaml")

    def test_converter(self):
        self.assertEqual(Converter.convert(integer), integer)
        self.assertEqual(Converter.convert(string), string)
        self.assertEqual(Converter.convert(c), c)
        self.assertEqual(Converter.convert(boolean), boolean)

        self.assertEqual(Converter.convert(simple_func), Converter.convert_function(simple_func))
        self.assertEqual(Converter.convert(arguments_func), Converter.convert_function(arguments_func))
        self.assertEqual(Converter.convert(butoma_func), Converter.convert_function(butoma_func))

        self.assertEqual(Converter.convert(math), Converter.convert_module(math))

    def test_json(self):
        self.assertEqual(self.json.loads(self.json.dumps(integer)), integer)
        self.assertEqual(self.json.loads(self.json.dumps(string)), string)
        self.assertEqual(self.json.loads(self.json.dumps(c)), c)
        self.assertEqual(self.json.loads(self.json.dumps(boolean)), boolean)

        self.assertEqual(self.json.loads(self.json.dumps(simple_func))(), simple_func())
        self.assertEqual(self.json.loads(self.json.dumps(arguments_func))(1, 2, 3), arguments_func(1, 2, 3))
        self.assertEqual(self.json.loads(self.json.dumps(butoma_func))(2), butoma_func(2))

    def test_yaml(self):
        self.assertEqual(self.yaml.loads(self.yaml.dumps(integer)), integer)
        self.assertEqual(self.yaml.loads(self.yaml.dumps(string)), string)
        self.assertEqual(self.yaml.loads(self.yaml.dumps(c)), c)
        self.assertEqual(self.yaml.loads(self.yaml.dumps(boolean)), boolean)

        self.assertEqual(self.yaml.loads(self.yaml.dumps(simple_func))(), simple_func())
        self.assertEqual(self.yaml.loads(self.yaml.dumps(arguments_func))(1, 2, 3), arguments_func(1, 2, 3))
        self.assertEqual(self.yaml.loads(self.yaml.dumps(butoma_func))(2), butoma_func(2))

    def test_toml(self):
        self.assertEqual(self.toml.loads(self.toml.dumps(integer)), {})
        self.assertEqual(self.toml.loads(self.toml.dumps(string)), {})
        self.assertEqual(self.toml.loads(self.toml.dumps(c)), {})
        self.assertEqual(self.toml.loads(self.toml.dumps(boolean)), {})

        self.assertEqual(self.toml.loads(self.toml.dumps(dict_test)), dict_test)
