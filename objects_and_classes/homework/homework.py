"""
Вам небхідно написати 3 класи. Колекціонери Гаражі та Автомобілі.
Звязкок наступний один колекціонер може мати багато гаражів.
В одному гаражі може знаходитися багато автомобілів.

Автомобіль має наступні характеристики:
    price - значення типу float. Всі ціни за дефолтом в одній валюті.
    type - одне з перечисленних значеннь з CARS_TYPES в docs.
    producer - одне з перечисленних значеннь в CARS_PRODUCER.
    number - значення типу UUID. Присвоюється автоматично при створенні автомобілю.
    mileage - значення типу float. Пробіг автомобіля в кілометрах.


    Автомобілі можна перівнювати між собою за ціною.
    При виводі(logs, print) автомобілю повинні зазначатися всі його атрибути.

    Автомобіль має метод заміни номеру.
    номер повинен відповідати UUID

Колекціонер має наступні характеристики
    name - значення типу str. Його ім'я
    garages - список з усіх гаражів які належать цьому Колекціонеру. Кількість гаражів за замовчуванням - 0
    register_id - UUID; Унікальна айдішка Колекціонера.

    Повинні бути реалізовані наступні методи:
    hit_hat() - повертає ціну всіх його автомобілів.
    garages_count() - вертає кількість гаріжів.
    сars_count() - вертає кількість машиню
    add_car() - додає машину у вибраний гараж. Якщо гараж не вказаний, то додає в гараж, де найбільше вільних місць.
    Якщо вільних місць немає повинне вивести повідомлення про це.

    Колекціонерів можна порівнювати за ціною всіх їх автомобілів.


    Гараж має наступні характеристики:

    town - одне з перечислениз значеннь в TOWNS
    cars - список з усіх автомобілів які знаходяться в гаражі
    places - значення типу int. Максимально допустима кількість автомобілів в гаражі
    owner - значення типу UUID. За дефолтом None.


    Повинен мати реалізованими наступні методи

    add(car) -> Добавляє машину в гараж, якщо є вільні місця
    remove(cat) -> Забирає машину з гаражу.
    hit_hat() -> Вертає сумарну вартість всіх машин в гаражі
"""


from constants import CARS_TYPES, CARS_PRODUCER, TOWNS, NAMES
import random
import uuid
from itertools import count


class Cesar:
    """Cesars class
    Available methods:
    1. Number_changer: change car unique ID number
    2.
    """

    def __init__(self):
        """"""
        self.name = random.choice(NAMES)
        self.garages = []
        self.registerID = uuid.uuid4()

    def __str__(self):
        return f'Owners name- {self.name}\nID- {self.registerID}\nList of garages- {self.garages}'

    def __repr__(self):
        return f'"{vars(self)}"'

    def add_garage(self, garage):
        if garage.owner == None:
            self.garages.append(garage)
            garage.owner = self.registerID
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

    def __init__(self, price, mileage):
        """Initiate our class with constructor"""
        self.price = float(price)
        self.mileage = float(mileage)
        self.type = random.choice(CARS_TYPES)
        self.producer = random.choice(CARS_PRODUCER)
        self.number = uuid.uuid4()

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


class Garage:
    """Class for garage
    Available methods:
    1.
    2.
    """
    number = count(1, 1)

    def __init__(self, places, owner=None):
        """Class constructor"""
        self.places = places
        self.owner = owner
        self.town = random.choice(TOWNS)
        self.cars = []
        self.number = next(Garage.number)

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



car1 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car2 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car3 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car4 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car5 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car6 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car7 = Car(random.randint(1000, 50000), random.randint(0, 100000))
car8 = Car(random.randint(1000, 50000), random.randint(0, 100000))

garage1 = Garage(5)
garage1.add(car1)
garage1.add(car2)



garage2 = Garage(8)
garage2.add(car4)
garage2.add(car5)

garage3 = Garage(3)
garage3.add(car6)
garage3.add(car7)
garage3.add(car8)


cesar1 = Cesar()
cesar2 = Cesar()



# if __name__ == '__main__':

print('________________________TESTING________________________', end='\n')

print(car1, end='\n\n')


print('Class Car methods')

car1.number_changer(uuid.uuid4())
print('Test change_number method', end='\n\n')
print(car1, end='\n\n')
print('As you can see ID number changed successfully', end='\n\n')

print('Testing car comparison', end='\n')
print(car1 > car2, end='\n\n')

print('______________________Garage testing___________________', end='\n\n')
print(garage1)

print('Remove car from garage', end='\n')
garage1.remove(car1)
print(garage1, end='\n\n')
print('As you can see car removed from the garage', end='\n\n')

print('Hit_hat method testing')
print(garage1.hit_hat(), end='\n\n')

print('______________________Cesar testing____________________', end='\n\n')

print(cesar1, end='\n\n')

print('Add garage and car, and test adding car to the garage with free spaces', end='\n\n')
cesar1.add_garage(garage1)
cesar1.add_car(car1)

print(cesar1)

print('Testing methods garage_count, car_count, and hit_hat', end='\n')

print(cesar1.garages_count())
print(cesar1.cars_count())
print(cesar1.hit_hat(), end='\n\n')

print('Testing of comparing cesars')
print(cesar1 > cesar2)



