from Modules.serializers.json_serializer import JSONSerializer
from Data.Classes.classes import Person

persons = []
for i in range(1, 5):
    persons.append(Person(f'Person{i}', f'person{i}@gmail.com', f'+37529{i}{i}{i}{i}{i}{i}{i}', 10*i))

serialize_persons = []
for person in persons:
    serialize_persons.append(person.to_serializable())

serializer = JSONSerializer()
json = serializer.dumps(serialize_persons)
print(json)