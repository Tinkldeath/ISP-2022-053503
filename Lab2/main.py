from Modules.lib.factory.serializer_factory import SerializerFactory

serializer = SerializerFactory.create_serializer("json")
j = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")
serializer = SerializerFactory.create_serializer("yaml")
serializer.dump(j, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.yml")
y = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.yml")
serializer = SerializerFactory.create_serializer("toml")
t = serializer.load("/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.toml")
print(t)
