from flask import Flask
from main import main
from config import Configuration
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask import request


app = Flask(__name__)
app.config.from_object(Configuration)
# app.register_blueprint(main)

api = Api(app)
parser_companies = reqparse.RequestParser(bundle_errors=True)#bundle_errors позволяет получить все ошибки ( если у нас несколько add.arguments)
parser_companies.add_argument('page', type=int, help='Wrong value')
# аргументы  action='append'- добавляет значения одинаковых аргументов в словарь
# для того, чтобы парсить аргументы с разных источников указываем локейшен:
# parser.add_argument(location = 'form', 'args', 'header', 'cookies', 'files')
# parser_inherited = parser_companies.copy() Наследование от существующего парсера

class RestTest(Resource):
    def get(self):
        return {'key': 'value'}

    def post(self):
        """Пример с кодом ответа и хедером"""
        return 'post', 318, {'custom_header': 'value'}


a = ['Apple', 'Amazon', 'Alphabet', 'Microsoft']


class Companies(Resource):
    def get(self):
        args = parser_companies.parse_args(strict=True)#Стрикт тру для ограничения входящих аргументов только теми, что мы указали в парсер адд аргумент
        print(args)
        response = dict()
        for i, element in enumerate(a):
            response[i] = element
        return response

    def post(self, value):
        a.append(value)
        return a

    def put(self):
        import json
        data = json.loads(request.data)
        company = data.get('company')
        position = data.get('position') -1

        a.remove(company)
        a.insert(position, company)
        return 'Successful'

    def delete(self, value):
        a.remove(value)
        return 'Successful'

# создаем структуру обьекта, для передачи в качестве аргументов
structure_fish = {
    'name': fields.String(attribute='name for customer'), #указали атрибут для того, чтобы отобразить клиенту другое имя переменной
    'size': fields.String
}


class Fish:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class GetFish(Resource):
    @marshal_with(structure_fish)
    def get(self):
        fish = Fish('Carp', '20cm')
        return fish


api.add_resource(RestTest, '/')
api.add_resource(Companies, '/companies', '/companies/<value>')
api.add_resource(GetFish, '/fish')


if __name__ == '__main__':
    app.run()
