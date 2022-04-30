from Modules.lib.serializers.json_serializer import JSONSerializer
from Modules.classes.classes import Person, Company

companies = list()
persons = list()

for i in range(1, 6):
    persons.append(Person(f'Person{i}', f'person{i}@gmail.com', f'+37529{i}{i}{i}{i}{i}{i}{i}', 20*i))

for i in range(1, 4):
    companies.append(Company(f'Company {i}', Person(f'Director {i}', f'director{i}@gmail.com', f'+37529{i}{i}{i}{i}{i}{i}{i}', 30), persons, True).to_serializable())

json = dict()
json['companies'] = companies
json['complete'] = True
json['moderated'] = False
json['sender'] = None

serializer = JSONSerializer()
serializer.dump(json, '/Users/dima/Documents/BSUIR/Python/ISP-2022-053503/Lab2/Data/data.json')
