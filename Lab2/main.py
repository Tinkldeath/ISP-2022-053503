from Modules.lib.factory.serializer_factory import SerializerFactory
from Modules.functions.functions import simple_func, inc, fibonacci, get_vars

serializer = SerializerFactory.create_serializer("json")
serializer.dump(inc, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")
increment = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")

serializer.dump(simple_func, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")
simple = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")

serializer.dump(fibonacci, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")
fib = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")

serializer.dump(get_vars, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")
vars = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")

simple(123)
print(fib(7))
print(inc(5))
print(vars(5))
