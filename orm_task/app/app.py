from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from orm_task import properties


class App:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)

            app = Flask(__name__)
            app.config.from_object(properties)

            cls.instance.__db = SQLAlchemy(app)
            cls.instance.__app = app

        return cls.instance

    def getApp(self):
        return self.__app

    def getDb(self):
        return self.__db
