from datetime import datetime
from os import uname
from sys import version

from flask import render_template, request

from app import App

app = App().getApp()


@app.route('/')
def index():
    return render_template("main.html", menu=App.getMenu(),
                           operating_system=uname().sysname,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route("/about")
def about():
    return render_template("about.html", menu=App.getMenu())


@app.route("/score")
def score():
    return render_template("score.html", menu=App.getMenu())


if __name__ == '__main__':
    app.run(debug=True)
