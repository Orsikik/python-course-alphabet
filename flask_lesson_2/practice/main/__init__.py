from flask import Blueprint


main = Blueprint('main', __name__)


@main.route('/')
def main_page():
    return 'Hello from blueprint'

