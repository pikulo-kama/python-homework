from typing import Dict
from flask_wtf import FlaskForm


def getUserFromSession():
    from flask import session

    return {
        'username': session.get('username'),
        'email': session.get('email')
    }


def addUserToSession(fields: Dict[str, str]):
    from flask import session

    for key, value in fields.items():
        session[key] = value


def userNotInSession():
    cookie = getUserFromSession()
    return cookie['username'] is None and cookie['email'] is None


def saveData(user: FlaskForm, dumpFile: str):
    from json import dump

    with open(dumpFile, 'a') as f:
        dump({
            'username': user.name.data,
            'email': user.email.data,
            'body': user.email.data,
        }, f)
        f.write('\r\n')
