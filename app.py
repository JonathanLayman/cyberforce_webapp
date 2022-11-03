from flask import Flask, render_template, request, session, redirect, escape, Blueprint
from flask_sqlalchemy import SQLAlchemy

# https://www.tutorialspoint.com/flask/flask_sessions.htm
# https://www.w3schools.com/howto/howto_css_example_website.asp
# https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/
# https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/

db = SQLAlchemy()

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("home.html", username=username)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("contact.html")


@app.route('/manufacturing')
def manufacturing():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("manufacturing.html")


@app.route('/solar')
def solar():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("solar.html")


@app.route('/login')
def login():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
