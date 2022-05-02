from Modules.lib.factory.serializer_factory import SerializerFactory

serializer = SerializerFactory.create_serializer("json")
s = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")
serializer = SerializerFactory.create_serializer("yaml")
serializer.dump(s, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.yml")
o = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.yml")
print(o)