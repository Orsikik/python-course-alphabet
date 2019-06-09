import psycopg2

connection = psycopg2.connect(user='cursor',
                              password='password',
                              host='localhost',
                              port='5432',
                              database='flask_db')
cursor = connection.cursor()
from_fruits = 'select * from products.fruits;'
from_vegetable = 'select * from products.vegetables;'

insert_fruit = """ INSERT INTO products.fruits (p_name, description, picture_link) VALUES (%s,%s,%s)"""
insert_vegetable = """ INSERT INTO products.vegetables (p_name, description, picture_link) VALUES (%s,%s,%s)"""


def fetch_from_fruits():
    data = []
    cursor.execute(from_fruits)
    result = cursor.fetchall()
    for row in result:
        unit = {'name': row[1],
                'description': row[2],
                'picture': row[3]
                }
        data.append(unit)
    return data


def fetch_from_vegatables():
    data = []
    cursor.execute(from_vegetable)
    result = cursor.fetchall()
    for row in result:
        unit = {'name': row[1],
                'description': row[2],
                'picture': row[3]
                }
        data.append(unit)
    return data


def insert_into_fruit(data):
    cursor.execute(insert_fruit, data)
    connection.commit()


def insert_into_vegetable(data):
    cursor.execute(insert_vegetable, data)
    connection.commit()


def delete_from_fruit(data):
        cursor.execute("DELETE FROM products.fruits WHERE p_name='{}'".format(data))
        connection.commit()


def delete_from_vegetable(data):
    cursor.execute("DELETE FROM products.vegetables WHERE p_name='{}'".format(data))
    connection.commit()


def delete(index, val):
    table_name = ('products.{}'.format(index))
    if index == 'vegetables':
        vegetables = fetch_from_vegatables()
        positive = [product.values() for product in vegetables if val in product.values()]
        if positive:
            cursor.execute("DELETE FROM {} WHERE p_name='{}'".format(table_name, val))
            connection.commit()
        else:
            raise ValueError
    if index == 'fruits':
        fruits = fetch_from_fruits()
        positive = [product.values() for product in fruits if val in product.values()]
        if positive:
            cursor.execute("DELETE FROM {} WHERE p_name='{}'".format(table_name, val))
            connection.commit()
        else:
            raise ValueError





