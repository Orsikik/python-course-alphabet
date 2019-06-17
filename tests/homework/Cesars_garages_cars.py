from constants import TOWNS, CARS_PRODUCER, CARS_TYPES, NAMES
import random
import uuid
import json
import pickle
from ruamel.yaml import YAML
from loggers import exception, logger
import psycopg2

connection = psycopg2.connect(user='cursor',
                              password='password',
                              host='localhost',
                              port='5432',
                              database='tests_db')
cursor = connection.cursor()


class Cesar:
    """Cesars class
    Available methods:
    1. Number_changer: change car unique ID number
    2.
    """
    @exception(logger)
    def __init__(self, name, garages, register_id):
        """"""
        self.name = name
        self.garages = garages
        self.register_id = register_id
        logger.info(f'Instance {self.name} of a class Cesar created')

    def __str__(self):
        return f'Owners name- {self.name}\nID- {self.register_id}\nList of garages- {self.garages}'

    def __repr__(self):
        return f'"{vars(self)}"'

    @exception(logger)
    def add_garage(self, garage):
        if garage.__class__ == Garage:
            if garage.owner == None:
                self.garages.append(garage)
                garage.owner = self.register_id
                logger.info(f'Garage {garage.number} added')
            else:
                return "This garage already has a owner"
        else:
            return 'You can add only instance of a Garage class'

    @exception(logger)
    def add_car(self, car, garage=None):
        def max_places():
            free_places = max([garages.places for garages in self.garages])
            for i in self.garages:
                if i.places == free_places:
                    return i
        if garage == None:
            garage = max_places()
            return garage.add(car)
            logger.info(f'Car added to the garage')
        elif garage in self.garages:
            return garage.add(car)
            logger.info(f'Car added to the garage')
        else:
            return "This garage doesn't exist, or belongs to another owner"

    def garages_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum([len(garage.cars) for garage in self.garages])

    def hit_hat(self):
        return sum([sum([car.price for car in garage.cars]) for garage in self.garages])

    @exception(logger)
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
        logger.info(f"Instance name {self.name} sent to dict")
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

class Garage:
    """Class for garage
    Available methods:
    1.
    2.
    """

    @exception(logger)
    def __init__(self, places, owner, town, cars, number):
        """Class constructor"""
        self.places = places
        self.owner = owner
        self.town = town
        self.cars = list(cars)
        self.number = number
        logger.info(f'Created instance of a class Garage with number {self.number}')

    @exception(logger)
    def add(self, car):
        if car.__class__ == Car:
            if self.places > 0:
                self.cars.append(car)
                self.places -= 1
                car.garage_number_changer(self.number)
                logger.info(f'Car {car.number} added to garage {self.number}')
            else:
                return 'There is no free places in the garage'
        else:
            return 'You can add only an instance of class Car'

    @exception(logger)
    def remove(self, car):
        if car.__class__ == Car:
            if car in self.cars:
                self.cars.remove(car)
                self.places += 1
                logger.info(f'Car {car.number} removed from garage {self.number}')
                return 'The car has been removed'
            else:
                return 'There is no this car, in this garage'
        else:
            return 'You can add only an instance of class Car'

    @exception(logger)
    def hit_hat(self):
        return sum([car.price for car in self.cars])

    @exception(logger)
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
        logger.info(f'Instance of a class Garage {self.number} sent to dict')
        return obj_dict

    def __str__(self):
        return f'Garage characteristics: \nOwner- {self.owner}\nTown- {self.town}\n'\
               f'Free places- {self.places}\nNumber-{self.number}\nCars- {self.cars} '

    def __repr__(self):
        return f'"{vars(self)}"'

class Car:
    """Class for cars
    Available methods:
    1. number_changer: change car unique ID number
    2. """

    @exception(logger)
    def __init__(self, price, mileage, type, producer, number, garage_number=None):
        """Initiate our class with constructor"""
        self.price = float(price)
        self.mileage = float(mileage)
        self.type = type
        self.producer = producer
        self.number = number
        self.garage_number = garage_number
        logger.info(f'Created instance of a class Car, number{self.number}')

    @exception(logger)
    def number_changer(self, another_number):
        """change car unique ID number"""
        if type(another_number) == uuid.UUID:
            logger.info(f'Car number {self.number} change it to {another_number}')
            self.number = another_number
        else:
            raise ValueError('Not uuid number')

    def garage_number_changer(self, number):
        self.garage_number = number

    @exception(logger)
    def obj_to_dict(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__
        }
        obj_dict.update(self.__dict__)
        logger.info(f'Instance class Car, number {self.number} sent to dict')
        return obj_dict

    def __str__(self):
        """Override class description"""
        return f'Car characteristics: \nProducer- {self.producer} \nType- {self.type}\n' \
               f'Car price- {self.price} $\nMileage- {self.mileage} km \nID- {self.number}\nGarage_n {self.garage_number}'

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


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex
        if isinstance(obj, Car):
            return {"__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    "price": obj.price,
                    "type": obj.type,
                    "producer": obj.producer,
                    "number": obj.number,
                    "mileage": obj.mileage}
        if isinstance(obj, Garage):
            return {"__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    "places": obj.places,
                    "town": obj.town,
                    "cars": obj.cars}
        if isinstance(obj, Cesar):
            return {"__class__": obj.__class__.__name__,
                    "__module__": obj.__module__,
                    "name": obj.name,
                    "register_id": obj.register_id,
                    "garages": obj.garages}
        return json.JSONEncoder.default(self, obj)

    # def default(self, obj):
    #     if isinstance(obj, uuid.UUID):
    #         return obj.hex
    #     return json.JSONEncoder.default(self, obj)


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


def obj_hook(dic):
    return dict(dic)


def new_dict_t_obj(dic):
    name = dic['name']
    register_id = uuid.UUID(dic['register_id'], version=4)
    garages = dic['garages']
    cesar = Cesar(name, *garages, register_id)
    return cesar


def cesar_to_db(cesar):
    register_id = str(cesar.register_id)
    cesars_name = cesar.name
    table_insert_cesar = "INSERT INTO cesar(register_id, name) VALUES(%s, %s)"
    cursor.execute(table_insert_cesar, [register_id, cesars_name])
    connection.commit()
    if cesar.garages:
        for garage in cesar.garages:
            number = str(garage.number)
            places = garage.places
            town = garage.town
            owner = str(garage.owner)
            table_insert_garage = "INSERT INTO garages(number, places, town, owner) " \
                                  "VALUES (%s, %s, %s, %s)"
            cursor.execute(table_insert_garage, (number, places, town, owner))
            connection.commit()
    for garage in cesar.garages:
        if garage.cars:
            for car in garage.cars:
                number = str(car.number)
                price = car.price
                mileage = car.mileage
                car_type = car.type
                producer = car.producer
                garage_number = str(car.garage_number)
                table_insert_car = "INSERT INTO cars(number, price, mileage, car_type, producer, garage_number) " \
                                   "VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(table_insert_car, (number, price, mileage, car_type, producer, garage_number))
                connection.commit()
    cursor.close()


def cesar_from_db(number):
    comand = "SELECT * FROM cesar WHERE register_id=%s"
    cursor.execute(comand, [number])
    return cursor.fetchall()


if __name__ == "__main__":

    car1 = Car(2000, 10000, random.choice(CARS_TYPES), random.choice(CARS_PRODUCER), uuid.uuid4())
    car2 = Car(2000, 10000, random.choice(CARS_TYPES), random.choice(CARS_PRODUCER), uuid.uuid4())
    garage1 = Garage(2, None, random.choice(TOWNS), [], uuid.uuid4())
    garage2 = Garage(2, None, random.choice(TOWNS), [], uuid.uuid4())
    collector1 = Cesar(random.choice(NAMES), [], uuid.uuid4())
    collector2 = Cesar(random.choice(NAMES), [], uuid.uuid4())

    collector1.add_garage(garage1)
    collector1.add_car(car1)
    collector1.add_car(car2)


# ####################JSON Serialization TO STR##########################
#     serial_str_car = json.dumps(car1.obj_to_dict(), cls=JsonEncoder, indent=4)
#     serial_str_garage = json.dumps(garage1.obj_to_dict(), cls=JsonEncoder, indent=4)
#     serial_str_cesar = json.dumps(collector1.obj_to_dict(), cls=JsonEncoder, indent=4)
#
#     deserial_str_car = json.loads(serial_str_car, object_hook=dict_to_obj)
#     deserial_str_garage = json.loads(serial_str_garage, object_hook=dict_to_obj)
#     deserial_str_cesar = json.loads(serial_str_cesar, object_hook=obj_hook)

    # print('___________JSON str Deserialized____________', end='\n\n')
    # print(deserial_str_car)
    # print(deserial_str_garage)
    # # print(deserial_str_cesar)
    # new_cesar = new_dict_t_obj(deserial_str_cesar)

#
#
#     print("####################JSON Serialization TO FILE##########################", end='\n\n')
#     with open('serial_file_car.json', 'w') as file:
#         json.dump(car1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
#     with open('serial_file_garage.json', 'w') as file:
#         json.dump(garage1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
#     with open('serial_file_collector.json', 'w') as file:
#         json.dump(collector1.obj_to_dict(), file, cls=JsonEncoder, indent=4)
#
#     with open('serial_file_car.json', 'r') as file:
#         deserial_file_car = json.load(file, object_hook=dict_to_obj)
#     with open('serial_file_garage.json', 'r') as file:
#         deserial_file_garage = json.load(file, object_hook=dict_to_obj)
#     with open('serial_file_collector.json', 'r') as file:
#         deserial_file_collector = json.load(file, object_hook=dict_to_obj)
#
#     print('___________JSON files Deserialized____________', end='\n\n')
#     print(deserial_file_car)
#     print(deserial_file_garage)
#     print(deserial_file_collector, end='\n\n')
#
#     print("#################### Pickle ##########################", end='\n\n')
#
#     with open("pickle_car.txt", "wb") as file:
#         pickle.dump(car1, file)
#     with open("pickle_garage.txt", "wb") as file:
#         pickle.dump(garage1, file)
#     with open("pickle_collector.txt", "wb") as file:
#         pickle.dump(collector1, file)
#
#     with open("pickle_car.txt", "rb") as file:
#         pickle_car = pickle.load(file)
#     with open("pickle_garage.txt", "rb") as file:
#         pickle_garage = pickle.load(file)
#     with open("pickle_collector.txt", "rb") as file:
#         pickle_collector = pickle.load(file)
#
#
#     print(pickle_car)
#     print(pickle_garage)
#     print(pickle_collector, end='\n\n')
#
#     print("#################### Yaml ##########################", end='\n\n')
#
#     yaml = YAML(typ='unsafe')
#
#     with open("yaml_car.yaml", "w") as file:
#         yaml.dump(car1, file)
#     with open("yaml_garage.yaml", "w") as file:
#         yaml.dump(garage1, file)
#     with open("yaml_collector.yaml", "w") as file:
#         yaml.dump(collector1, file)
#
#     with open("yaml_car.yaml", "r") as file:
#         yaml_car = yaml.load(file)
#     with open("yaml_garage.yaml", "r") as file:
#         yaml_garage = yaml.load(file)
#     with open("yaml_collector.yaml", "r") as file:
#         yaml_collector = yaml.load(file)
#
#     print(yaml_car)
#     print(yaml_garage)
#     print(yaml_collector)