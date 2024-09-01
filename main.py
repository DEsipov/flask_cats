from flask import Flask, jsonify, render_template
from flask_migrate import Migrate

# Импортируем класс для работы с ORM:
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключаем БД SQLite:

from settings import Config

app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
