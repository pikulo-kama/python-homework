from datetime import datetime
from os import uname
from sys import version

from flask import render_template, request, flash, redirect, url_for

from .app import App
from .forms import ContactForm
from .helper import *

app = App().getApp()
menu = App.getMenu()

DUMP_FILE = 'userdata.txt'


@app.route('/')
def index():
    return render_template("main.html", menu=menu,
                           operating_system=uname().sysname,
                           user_agent=request.user_agent,
                           python_version=version,
                           time=datetime.now().strftime("%H:%M:%S")
                           )


@app.route("/about")
def about():
    return render_template("about.html", menu=menu)


@app.route("/score")
def score():
    return render_template("score.html", menu=menu)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':

        if userNotInSession():

            if form.validate_on_submit():

                addUserToSession({
                    'username': form.name.data,
                    'email': form.email.data
                })

                saveData(form, DUMP_FILE)

                flash(message="Success information saved")
                return redirect(url_for('contact'))

            else:
                flash(message="Error during data validation")

        else:

            cookie = getUserFromSession()

            form.name.data = cookie['username']
            form.email.data = cookie['email']

            return redirect(url_for('contact'))

    return render_template('contact.html', menu=menu, form=form, cookie=getUserFromSession())
