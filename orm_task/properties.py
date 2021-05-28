from os import environ, path

basedir = path.abspath(path.dirname(__file__))

SECRET_KEY = 'secret'
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = environ.get("FLASK_DATABASE_URI") or 'sqlite:///' + path.join(basedir, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
