import math
from modules.factory import SerializerFactory

c = 42


def f(x):
    a = 123
    return math.sin(a*x*c)


serializer = SerializerFactory.create_serializer("json")
config = serializer.load("./config/config.json")
data_path = ""
form = ""

if config is not None:
    for key, value in config.items():
        if key == "data_folder":
            data_path += value
        elif key == "format":
            form += value
        else:
            continue
    if data_path != "" and form != "":
        serializer = SerializerFactory.create_serializer(config["format"])
        serializer.dump(f, f'{data_path}/data.{form.lower()}')
        foo = serializer.load(f'{data_path}/data.{form.lower()}')
        print(f'Function(2): {f(2)}')
        print(f'Serialized_function(2): {f(2)}')
