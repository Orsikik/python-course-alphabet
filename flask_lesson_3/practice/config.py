from flask_sqlalchemy import SQLAlchemy
from app import app

PG_USER = "cursor"
PG_PASSWORD = "password"
PG_HOST = "localhost"
PG_PORT = 5432
DB_NAME = "flask_db"
SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"

db = SQLAlchemy(app)