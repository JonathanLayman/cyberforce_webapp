#!/usr/bin/python3
from flask import Flask, render_template, request, session, redirect, url_for, escape, flash, send_file
from werkzeug.utils import secure_filename
import os
import json
from really_horible_user_implementation import auth_user
from ftp_connector import ftp_retrieve_contents, ftp_upload, ftp_download

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
    if request.method == 'POST':
        # # handle form data
        try:
            with open('messages.json') as file:
                messages = json.load(file)
        except json.decoder.JSONDecodeError:
            messages = {}
        print(len(messages))
        messages[len(messages) + 1] = {
            "Name": request.form['Name'],
            "Email": request.form['Email'],
            "Phone": request.form['Phone'],
        }
        with open("messages.json", "w") as outfile:
            json.dump(messages, outfile)

        # handle file data
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(f"{filename}")
            ftp_upload(filename)
            os.remove(filename)
            return render_template("contact.html", username=username, submitted=True)
    return render_template("contact.html", username=username, submitted=False)


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
        # Get emails from json file
        try:
            with open('messages.json') as file:
                messages = json.load(file)
        except json.decoder.JSONDecodeError:
            messages = {}
        emails = messages
        return render_template("admin.html", username=session['username'], files=ftp_list, emails=emails)
    else:
        return render_template("user.html", username=session['username'])


@app.route('/download/<filename>')
def download_file(filename):
    if session['username'] == 'plank':
        ftp_download(filename=filename)
        return send_file(filename, as_attachment=True)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80)
    app.run()