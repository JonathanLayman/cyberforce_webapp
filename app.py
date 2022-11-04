from flask import Flask, render_template, request, session, redirect, url_for, escape
from really_horible_user_implementation import auth_user
from ftp_connector import ftp_retrieve_contents

# https://www.tutorialspoint.com/flask/flask_sessions.htm
# https://www.w3schools.com/howto/howto_css_example_website.asp
# https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/
# https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/

app = Flask(__name__)
app.secret_key = 'Super Random String'

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
    return render_template("contact.html", username=username)


@app.route('/manufacturing')
def manufacturing():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("manufacturing.html", username=username)


@app.route('/solar')
def solar():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    return render_template("solar.html", username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    error = None
    if request.method == 'POST':
        if auth_user(request.form['username'].lower(), request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('user'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("login.html", username=username, error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/user')
def user():
    # check for admin user
    if session['username'] == 'plank':
        # Get contents of FTP Server
        ftp_list = ftp_retrieve_contents()
        emails = ["message1", "message2"]
        return render_template("admin.html", username=session['username'], files=ftp_list, emails=emails)
    else:
        return render_template("user.html", username=session['username'])


if __name__ == '__main__':
    app.run()
