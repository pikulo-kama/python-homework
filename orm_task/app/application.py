from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from orm_task import properties


class App:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)

            app = Flask(__name__)
            app.config.from_object(properties)
            db = SQLAlchemy(app)

            cls.instance.__db = db
            cls.instance.__app = app
            cls.instance.__migrate = Migrate(app, db)
            cls.instance.__manager = Manager(app, MigrateCommand)

        return cls.instance

    def getApp(self):
        return self.__app

    def getDb(self):
        return self.__db

    def getMigrateHelper(self):
        return self.__migrate

    def getManager(self):
        return self.__manager
