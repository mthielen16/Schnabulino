import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mthie:9P4ns3n#16@164.92.192.79/schnabulino_user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    einrichtung = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




