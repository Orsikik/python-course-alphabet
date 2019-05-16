

"""
Для попереднього домашнього завдання.

Для класів Колекціонер Машина і Гараж написати методи, які зберігають стан обєкту в файли формату
yaml, json, pickle відповідно.

Для класів Колекціонер Машина і Гараж написати методи, які конвертують обєкт в строку формату
yaml, json, pickle відповідно.

Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) строки відповідно

Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) файлу відповідно

Advanced
Добавити опрацьовку формату ini

"""

from objects_and_classes.homework.constants import *
import random
import uuid
from itertools import count
import json
import pickle
from ruamel.yaml import YAML

class Cesar:
    """Cesars class
    Available methods:
    1. Number_changer: change car unique ID number
    2.
    """

    def __init__(self, name, garages, register_id):
        """"""
        self.name = name
        self.garages = list(garages)
        self.register_id = register_id

    def __str__(self):
        return f'Owners name- {self.name}\nID- {self.register_id}\nList of garages- {self.garages}'

    def __repr__(self):
        return f'"{vars(self)}"'

    def add_garage(self, garage):
        if garage.owner == None:
            self.garages.append(garage)
            garage.owner = self.register_id
        else:
            print("This garage already has a owner")

    def add_car(self, car, garage=None):
        def max_places():
            free_places = max([garages.places for garages in self.garages])
            for i in self.garages:
                if i.places == free_places:
                    return i
        if garage == None:
            garage = max_places()
            garage.add(car)
        elif garage in self.garages:
            garage.add(car)
        else:
            print("This garage doesn't exist, or belongs to another owner")

    def garages_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum([len(garage.cars) for garage in self.garages])

    def hit_hat(self):
        return sum([sum([car.price for car in garage.cars]) for garage in self.garages])

    def obj_to_dict(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__
        }
        obj_dict.update(self.__dict__)

        garages_serialized = []
        for garage in self.garages:
            garages_serialized.append(garage.obj_to_dict())
        obj_dict.update({'garages': garages_serialized})
        return obj_dict

    def __le__(self, other):
        return self.hit_hat() <= other.hit_hat()

    def __lt__(self, other):
        return self.hit_hat() < other.hit_hat()

    def __ge__(self, other):
        return self.hit_hat() >= other.hit_hat()

    def __gt__(self, other):
        return self.hit_hat() > other.hit_hat()

    def __eq__(self, other):
        return self.hit_hat() == other.hit_hat()

class Car:
    """Class for cars
    Available methods:
    1. number_changer: change car unique ID number
    2. """

    def __init__(self, price, mileage, type, producer, number):
        """Initiate our class with constructor"""
        self.price = float(price)
        self.mileage = float(mileage)
        self.type = type
        self.producer = producer
        self.number = number

    def __str__(self):
        """Override class description"""
        return f'Car characteristics: \nProducer- {self.producer} \nType- {self.type}\n' \
               f'Car price- {self.price} $\nMileage- {self.mileage} km \nID- {self.number}'

    def __repr__(self):
        return f'"{vars(self)}"'

    def __le__(self, other):
        return self.price <= other.price

    def __lt__(self, other):
        return self.price < other.price

    def __ge__(self, other):
        return self.price >= other.price

    def __gt__(self, other):
        return self.price > other.price

    def __eq__(self, other):
        return self.price == other.price

    def number_changer(self, another_number):
        """change car unique ID number"""

        if type(another_number) == uuid.UUID:
            self.number = another_number
        else:
            raise TypeError

    def comparison(self, price1, price2):
        if price1 == price2:
            print('Cars price are equal')
        elif price1 > price2:
            print('First car are more expensive')
        elif price1 < price2:
            print('First car are cheaper')

    def obj_to_dict(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__
        }
        obj_dict.update(self.__dict__)
        return obj_dict


class Garage:
    """Class for garage
    Available methods:
    1.
    2.
    """

    def __init__(self, places, owner, town, cars, number):
        """Class constructor"""
        self.places = places
        self.owner = owner
        self.town = town
        self.cars = list(cars)
        self.number = number

    def __str__(self):
        return f'Garage characteristics: \nOwner- {self.owner}\nTown- {self.town}\n'\
               f'Free places- {self.places}\nNumber-{self.number}\nCars- {self.cars} '

    def __repr__(self):
        return f'"{vars(self)}"'

    def add(self, car):
        if self.places > 0:
            self.cars.append(car)
            self.places -= 1
        else:
            print('There is no free places in the garage')

    def remove(self, car):
        if car in self.cars:
            self.cars.remove(car)
            self.places += 1
            print('The car has been removed')
        else:
            print('There is no this car, in this garage')

    def hit_hat(self):
        return sum([car.price for car in self.cars])

    def obj_to_dict(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__
        }
        obj_dict.update(self.__dict__)

        cars_serialized = []
        for car in self.cars:
            cars_serialized.append(car.obj_to_dict())
        obj_dict.update({'cars': cars_serialized})
        return obj_dict

# JSON Class

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def dict_to_obj(dic):
    if "number" or "register_id" in dic:
        dic.update({key: uuid.UUID(value) for key, value in dic.items()
                         if key == 'number' or key == 'register_id'})
    if "__class__" in dic:
        class_name = dic.pop("__class__")
        module_name = dic.pop("__module__")
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        obj = class_(**dic)
    else:
        obj = dic
    return obj


if __name__ == "__main__":

    car1 = Car(2000, 10000, random.choice(TOWNS), random.choice(CARS_PRODUCER), uuid.uuid4())
    car2 = Car(2000, 10000, random.choice(TOWNS), random.choice(CARS_PRODUCER), uuid.uuid4())
    garage1 = Garage(2, None, random.choice(TOWNS), [], uuid.uuid4())
    collector1 = Cesar(random.choice(NAMES), [], uuid.uuid4())

    collector1.add_garage(garage1)
    collector1.add_car(car1)



####################JSON Serialization TO STR##########################
    serial_str_car = json.dumps(car1.obj_to_dict(), cls=JsonEncoder, indent=4)
    serial_str_garage = json.dumps(garage1.obj_to_dict(), cls=JsonEncoder, indent=4)
    serial_str_cesar = json.dumps(collector1.obj_to_dict(), cls=JsonEncoder, indent=4)

    deserial_str_car = json.loads(serial_str_car, object_hook=dict_to_obj)
    deserial_str_garage = json.loads(serial_str_garage, object_hook=dict_to_obj)
    deserial_str_cesar = json.loads(serial_str_cesar, object_hook=dict_to_obj)

    print('___________JSON str Deserialized____________', end='\n\n')
    print(deserial_str_car)
    print(deserial_str_garage)
    print(deserial_str_cesar, end='\n\n')


    print("####################JSON Serialization TO FILE##########################", end='\n\n')
    with open('serial_file_car.json', 'w') as file:
        json.dump(car1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
    with open('serial_file_garage.json', 'w') as file:
        json.dump(garage1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
    with open('serial_file_collector.json', 'w') as file:
        json.dump(collector1.obj_to_dict(), file, cls=JsonEncoder, indent=4)

    with open('serial_file_car.json', 'r') as file:
        deserial_file_car = json.load(file, object_hook=dict_to_obj)
    with open('serial_file_garage.json', 'r') as file:
        deserial_file_garage = json.load(file, object_hook=dict_to_obj)
    with open('serial_file_collector.json', 'r') as file:
        deserial_file_collector = json.load(file, object_hook=dict_to_obj)

    print('___________JSON files Deserialized____________', end='\n\n')
    print(deserial_file_car)
    print(deserial_file_garage)
    print(deserial_file_collector, end='\n\n')

    print("#################### Pickle ##########################", end='\n\n')

    with open("pickle_car.txt", "wb") as file:
        pickle.dump(car1, file)
    with open("pickle_garage.txt", "wb") as file:
        pickle.dump(garage1, file)
    with open("pickle_collector.txt", "wb") as file:
        pickle.dump(collector1, file)

    with open("pickle_car.txt", "rb") as file:
        pickle_car = pickle.load(file)
    with open("pickle_garage.txt", "rb") as file:
        pickle_garage = pickle.load(file)
    with open("pickle_collector.txt", "rb") as file:
        pickle_collector = pickle.load(file)


    print(pickle_car)
    print(pickle_garage)
    print(pickle_collector, end='\n\n')

    print("#################### Yaml ##########################", end='\n\n')

    yaml = YAML(typ='unsafe')

    with open("yaml_car.yaml", "w") as file:
        yaml.dump(car1, file)
    with open("yaml_garage.yaml", "w") as file:
        yaml.dump(garage1, file)
    with open("yaml_collector.yaml", "w") as file:
        yaml.dump(collector1, file)

    with open("yaml_car.yaml", "r") as file:
        yaml_car = yaml.load(file)
    with open("yaml_garage.yaml", "r") as file:
        yaml_garage = yaml.load(file)
    with open("yaml_collector.yaml", "r") as file:
        yaml_collector = yaml.load(file)

    print(yaml_car)
    print(yaml_garage)
    print(yaml_collector)

