import math
from modules.factory import SerializerFactory

c = 42
def f(x):
    a = 123
    return math.sin(a*x*c)

serializer = SerializerFactory.create_serializer("json")
serializer.dump(f, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.json")
foo = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/data/data.json")
print(f(2))
print(foo(2))