"""
Для попереднього домашнього завдання.
Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) файлу відповідно
Для класів Колекціонер Машина і Гараж написати методи, які зберігають стан обєкту в файли формату
yaml, json, pickle відповідно.
Для класів Колекціонер Машина і Гараж написати методи, які конвертують обєкт в строку формату
yaml, json, pickle відповідно.
Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) строки відповідно
Advanced
Добавити опрацьовку формату ini
"""


from objects_and_classes.homework import constants as c
import uuid
from functools import reduce
import json
import pickle
import configparser


class Cesar:
    def __init__(self, name, garages=0, register_id=None):
        self.name = str(name)
        self.garages = garages
        self.register_id = register_id if register_id else uuid.uuid4()

    def hit_hat(self):
        return sum([sum([car.price for car in garage.cars]) for garage in self.garages])

    def garages_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum([len([car for car in garage.cars]) for garage in self.garages])

    def add_car(self, new_car, garage=None):
        if garage is None:
            max_free_garage = reduce((lambda x, y: x if x.free_places() > y.free_places() else y), self.garages)
            # max_free_garage = [garage for garage in self.garages
            #                 if garage.free_places() == max(garage.free_places() for garage in self.garages)][0]
            if max_free_garage.free_places() > 0:
                return max_free_garage.cars.append(new_car)
            else:
                print("There's no free space at your garages for your car!")
        else:
            if garage.free_places() > 0:
               garage.cars.append(new_car)
            else:
                print("There's no free space at this garage for your car!")

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

    def __str__(self):
        return f"""
        Attributes of current Cesar:
            name: '{self.name}';
            total garages: '{len(self.garages)}';
            register_id: '{self.register_id}';
        """

    def __repr__(self):
        return f"""Cesar(name='{self.name}', garages='{len(self.garages)}')"""

    def __gt__(self, other):
        return self.hit_hat() > other.hit_hat()

    def __lt__(self, other):
        return self.hit_hat() < other.hit_hat()

    def __ge__(self, other):
        return self.hit_hat() >= other.hit_hat()

    def __le__(self, other):
        return self.hit_hat() <= other.hit_hat()

    def __eq__(self, other):
        return self.hit_hat() == other.hit_hat()

    def __ne__(self, other):
        return self.hit_hat() != other.hit_hat()


class Car:
    def __init__(self, price, type, producer, mileage, number=None):
        if type in c.CARS_TYPES and producer in c.CARS_PRODUCER:
            self.price = float(price)
            self.type = type
            self.producer = producer
            self.number = number if number else uuid.uuid4()
            self.mileage = float(mileage)
        else:
            print('Unknown car type or producer')

    def change_number(self, new_number):
        try:
            uuid.UUID(new_number, version=4)
            self.number = new_number
        except (ValueError, AttributeError, TypeError):
            print("It's not UUID number!")

    def obj_to_dict(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__
        }
        obj_dict.update(self.__dict__)
        return obj_dict

    def __str__(self):
        return f"""
        Attributes of current Car:
            price: '{self.price}';
            type: '{self.type}';
            producer: '{self.producer}';
            number: '{self.number}';
            mileage: '{self.mileage}';
        """

    def __repr__(self):
        return f"""Car(price='{self.price}', type='{self.type}', producer='{self.producer}', mileage='{self.mileage}')"""

    def __gt__(self, other):
        return self.price > other.price

    def __lt__(self, other):
        return self.price < other.price

    def __ge__(self, other):
        return self.price >= other.price

    def __le__(self, other):
        return self.price <= other.price

    def __eq__(self, other):
        return self.price == other.price

    def __ne__(self, other):
        return self.price != other.price


class Garage:
    def __init__(self, town, cars, places, owner=None):
        if town in c.TOWNS:
            self.town = town
            self.cars = cars
            self.places = int(places)
            self.owner = owner
        else:
            print('Unknown town name')

    def add_car(self, new_car):
        free_places = self.places - len(self.cars)
        if free_places > 0:
            free_places -= 1
            self.cars.append(new_car)
        else:
            print('Garage is full!')

    def remove_car(self, new_car):
        if new_car in self.cars:
            free_places = self.places - len(self.cars)
            if self.places - len(self.cars) < 0:
                print('How you even fit there so many cars!?')
            else:
                self.cars.remove(new_car)
                free_places += 1
        else:
            print('No such car in garage')

    def hit_hat(self):
        return sum([car.price for car in self.cars])

    def free_places(self):
        return self.places - len(self.cars)

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

    def __str__(self):
        return f"""
        Attributes of current Garage:
            town: '{self.town}';
            total cars: '{len(self.cars)}';
            places: '{self.places}';
            owner: '{self.owner}';
        """

    def __repr__(self):
        return f"""Garage(town='{self.town}', cars='{len(self.cars)}', places='{self.places}', owner='{self.owner}')"""


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def dict_to_obj(our_dict):
    if 'number' or 'register_id' in our_dict:
        our_dict.update({key: uuid.UUID(value) for key, value in our_dict.items()
                         if key=='number' or key=='register_id'})
    if "__class__" in our_dict:
        class_name = our_dict.pop("__class__")
        module_name = our_dict.pop("__module__")
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj


if __name__ == "__main__":

    car1 = Car(1001, "Diesel", "BMW",  1123)
    car2 = Car(2000, "Crossover", "BENTLEY", 5422)
    garage1 = Garage('Kiev', [car1, car2], 2, )
    garage2 = Garage('Prague', [car2], 12, )
    garage3 = Garage('Prague', [car2, car1], 10, )
    cesar1 = Cesar("Crappy", [garage1, garage2, garage3])
    cesar2 = Cesar("Another guy", [garage1])


# print('_____________________________json dump/load_____________________________')

# with open('car1.json', 'w') as file:
#     json.dump(car1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
# with open('car1.json', 'r') as file:
#     car1_from_file = json.load(file, object_hook=dict_to_obj)
# print(car1_from_file)
#
# with open('garage1.json', 'w') as file:
#     json.dump(garage1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
# with open('garage1.json', 'r') as file:
#     garage1_from_file = json.load(file, object_hook=dict_to_obj)
# print(garage1_from_file)
#
# with open('cesar1.json', 'w') as file:
#     json.dump(cesar1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
# with open('cesar1.json', 'r') as file:
#     cesar1_from_file = json.load(file, object_hook=dict_to_obj)
# print(cesar1_from_file)


# print('_____________________________json dumps/loads_____________________________')

car1_with_dupms = json.dumps(car1.obj_to_dict(), cls=JsonEncoder, indent=4)
print(car1_with_dupms)
decoding_car1_with_loads = json.loads(car1_with_dupms, object_hook=dict_to_obj)
print(decoding_car1_with_loads)

# garage1_with_dupms = json.dumps(garage1.obj_to_dict(), cls=JsonEncoder, indent=4)
# print(garage1_with_dupms)
# decoding_garage1_with_loads = json.loads(garage1_with_dupms, object_hook=dict_to_obj)
# print(decoding_garage1_with_loads)

# cesar1_with_dupms = json.dumps(cesar1.obj_to_dict(), cls=JsonEncoder, indent=4)
# print(cesar1_with_dupms)
# decoding_cesar1_with_loads = json.loads(cesar1_with_dupms, object_hook=dict_to_obj)
# print(decoding_cesar1_with_loads)
