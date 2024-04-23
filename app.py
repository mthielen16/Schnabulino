import os
from flask import Flask, render_template, request, redirect, url_for, flash, session


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)


# Zugelassene Benutzernamen und Passwörter
users = {
    'user1': 'pass1',
    'user2': 'pass2'
}

admins = {
    'PM': '1234',
    'MT': '1234'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('survey'))
        elif username in admins and admins[username] == password:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Falscher Benutzername oder Passwort')
    return render_template('login.html')

@app.route('/survey')
def survey():
    if not session.get('logged_in'):
        flash("Du musst dich erst einloggen!")
        return redirect(url_for('login'))
    return render_template('survey.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash("Du musst dich erst einloggen!")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))








