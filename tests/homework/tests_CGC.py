import unittest
import uuid
import Cesars_garages_cars as obj
import constants
import random
import json


class CarTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.car = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                           uuid.uuid4())
        self.uuid_number = uuid.uuid4()
        self.not_uuid = [['list'], [1, 2, 3], {'key': 'value'}, True, False, 123, 'test']
        self.car_dict = {
            '__class__': 'Car',
            '__module__': 'Cesars_garages_cars',
            'price': self.car.price,
            'garage_number': None,
            'mileage': self.car.mileage,
            'type': self.car.type,
            'producer': self.car.producer,
            'number': self.car.number
        }

    def test_number_changer_succ(self):
        # Testing function with valid data
        self.car.number_changer(self.uuid_number)
        self.assertEqual(self.uuid_number, self.car.number)

    def test_number_changer_err(self):
        # Testing function with wrong data
        with self.assertRaises(ValueError) as context:
            for i in self.not_uuid:
                self.car.number_changer(i)
            self.assertTrue('Not uuid number' in context.exception.args)

    def test_obj_to_dict(self):
        result = self.car.obj_to_dict()
        self.assertEqual(self.car_dict, result)


class GarageTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.garage = obj.Garage(2, random.choice(constants.NAMES),random.choice(constants.TOWNS),[],uuid.uuid4())
        self.car1 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                           uuid.uuid4())
        self.car2 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                           uuid.uuid4())
        self.car3 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.wrong_values = [['list'], [1, 2, 3], {'key': 'value'}, True, False, 123, 'test']
        self.garage_dict = {'__class__': 'Garage',
                            '__module__': 'Cesars_garages_cars',
                            'places': self.garage.places,
                            'owner': self.garage.owner,
                            'town': self.garage.town,
                            'cars': self.garage.cars,
                            'number': self.garage.number}

    def test_add_car_to_garage_succ(self):
        self.garage.add(self.car1)
        self.garage.add(self.car2)
        self.assertTrue(self.car1 in self.garage.cars)
        self.assertTrue(self.car2 in self.garage.cars)

    def test_add_no_free_places(self):
        self.garage.add(self.car1)
        self.garage.add(self.car2)
        result = self.garage.add(self.car3)
        self.assertEqual(result, 'There is no free places in the garage' )

    def test_add_wrong_value(self):
        for values in self.wrong_values:
            result = self.garage.add(values)
            self.assertEqual('You can add only an instance of class Car', result)

    def test_remove_car_succ(self):
        self.garage.add(self.car1)
        self.garage.remove(self.car1)
        self.assertTrue(self.garage.cars == [])

    def test_remove_car_err(self):
        for values in self.wrong_values:
            result = self.garage.remove(values)
            self.assertEqual('You can add only an instance of class Car', result)

    def test_hit_hat(self):
        self.garage.add(self.car1)
        self.garage.add(self.car2)
        result = self.garage.hit_hat()
        self.assertEqual(result, (self.car1.price+self.car2.price))

    def test_obj_to_dict(self):
        self.assertEqual(self.garage.obj_to_dict(), self.garage_dict)

class CesarTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.cesar1 = obj.Cesar(random.choice(constants.NAMES), [], uuid.uuid4())
        self.cesar2 = obj.Cesar(random.choice(constants.NAMES), [], uuid.uuid4())
        self.garage1 = obj.Garage(2, None, random.choice(constants.TOWNS), [], uuid.uuid4())
        self.garage2 = obj.Garage(2, random.choice(constants.NAMES), random.choice(constants.TOWNS), [], uuid.uuid4())
        self.garage3 = obj.Garage(2, None, random.choice(constants.TOWNS), [], uuid.uuid4())
        self.car1 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.car2 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.car3 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.wrong_values = [['list'], [1, 2, 3], {'key': 'value'}, True, False, 123, 'test']
        self.cesar_dict = {'__class__': 'Cesar',
                            '__module__': 'Cesars_garages_cars',
                            'name': self.cesar1.name,
                            'garages': self.cesar1.garages,
                            'register_id': self.cesar1.register_id}

    def test_add_garage_succ(self):
        self.cesar1.add_garage(self.garage1)
        self.assertTrue(self.garage1 in self.cesar1.garages)

    def test_add_garage_with_owner(self):
        self.assertEqual("This garage already has a owner", self.cesar1.add_garage(self.garage2))

    def test_add_garage_wrong_value(self):
        for value in self.wrong_values:
            self.assertEqual('You can add only instance of a Garage class', self.cesar1.add_garage(value))

    def test_add_car_succ(self):
        self.cesar1.add_garage(self.garage1)
        self.cesar1.add_car(self.car1, self.garage1)
        self.assertTrue(self.car1 in self.garage1.cars)

    def test_add_car_without_owner_succ(self):
        self.cesar1.add_garage(self.garage1)
        self.cesar1.add_garage(self.garage2)
        self.cesar1.add_car(self.car1)
        self.assertTrue(self.car1 in (self.garage1.cars or self.garage2.cars))

    def test_add_car_wrong_value(self):
        self.cesar1.add_garage(self.garage1)
        for values in self.wrong_values:
            self.assertEqual('You can add only an instance of class Car', self.cesar1.add_car(values))

    def test_garages_count(self):
        self.cesar1.add_garage(self.garage1)
        self.cesar1.add_garage(self.garage3)
        self.assertEqual(2, self.cesar1.garages_count())

    def test_cars_count(self):
        self.cesar1.add_garage(self.garage1)
        self.cesar1.add_car(self.car1)
        self.cesar1.add_car(self.car2)
        self.assertEqual(2, self.cesar1.cars_count())

    def test_hit_hat(self):
        self.cesar1.add_garage(self.garage1)
        self.cesar1.add_car(self.car1)
        self.cesar1.add_car(self.car2)
        self.assertEqual(self.cesar1.hit_hat(), (self.car1.price+self.car2.price))

    def test_obj_to_dict(self):
        self.assertEqual(self.cesar1.obj_to_dict(), self.cesar_dict)


class SerializationAndDeserializationTesting(unittest.TestCase):

    def setUp(self) -> None:
        self.cesar1 = obj.Cesar(random.choice(constants.NAMES), [], uuid.uuid4())
        self.cesar2 = obj.Cesar(random.choice(constants.NAMES), [], uuid.uuid4())
        self.garage1 = obj.Garage(2, None, random.choice(constants.TOWNS), [], uuid.uuid4())
        self.garage2 = obj.Garage(2, random.choice(constants.NAMES), random.choice(constants.TOWNS), [], uuid.uuid4())
        self.garage3 = obj.Garage(2, None, random.choice(constants.TOWNS), [], uuid.uuid4())
        self.car1 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.car2 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.car3 = obj.Car(6000, 20000, random.choice(constants.CARS_TYPES), random.choice(constants.CARS_PRODUCER),
                            uuid.uuid4())
        self.cesar1.add_garage(self.garage1)
        self.cesar1.add_car(self.car1)
        self.cesar1.add_car(self.car2)

    def test_serialization_and_de_to(self):
        serial_cesar = json.dumps(self.cesar1.obj_to_dict(), cls=obj.JsonEncoder, indent=4)
        deserial_cesar = json.loads(serial_cesar, object_hook=obj.obj_hook)
        new_cesar = obj.new_dict_t_obj(deserial_cesar)
        self.assertEqual(self.cesar1.name, new_cesar.name)
        self.assertEqual(self.cesar1.register_id, new_cesar.register_id)

