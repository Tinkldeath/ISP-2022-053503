import math
from modules.factory import SerializerFactory

c = 42


def f(x):
    a = 123
    return math.sin(a*x*c)


serializer = SerializerFactory.create_serializer("json")
serializer.dump(f, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.json")
foo_json = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.json")
print(foo_json(2))

serializer = SerializerFactory.create_serializer("yaml")
serializer.dump(f, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.yml")
foo_yaml = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.yml")
print(foo_yaml(2))

serializer = SerializerFactory.create_serializer("toml")
serializer.dump(f, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.toml")
foo_toml = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.toml")
print(foo_toml(2))