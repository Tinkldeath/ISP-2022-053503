from Modules.lib.serializers.json_serializer import JSONSerializer
from Modules.classes.classes import Person

d = dict()
persons = []
for i in range(1, 5):
    persons.append(Person(f'Person{i}', f'person{i}@gmail.com', f'+37529{i}{i}{i}{i}{i}{i}{i}', 10*i))

serialize_persons = []
for person in persons:
    serialize_persons.append(person.to_serializable())

d['persons'] = serialize_persons
d['bool1'] = False
d['bool2'] = True
serializer = JSONSerializer()
serializer.dump(d, "/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json")