import os
from flask import Flask, redirect, request, render_template, session, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import User, Trip, Place, UserTrip, connect_to_db, db


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

@app.route('/')
def index():
    """Display homepage"""

    return render_template('index.html')


@app.route('/login')
def login():
    """Display login page"""

    return render_template('login.html')


@app.route('/validate-login', methods=['POST'])
def validate_login():
    """Check that user entered correct email and password."""

    email = request.form.get('email')
    password = request.form.get('password')

    valid_user = User.query.filter_by(email=email, password=password).first()

    if valid_user:
        session['email'] = email
        return redirect(url_for('user_profile'))
    else:
        flash('Email or password is incorrect')
        return redirect(url_for('login'))


@app.route('/register')
def register():
    """Display Registration page."""

    return render_template('register.html')


@app.route('/validate-user', methods=['POST'])
def validate_new_user():
    """Validate new user and add to the database."""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('reg-email')
    password = request.form.get('reg-password')
    confirm_email = request.form.get('confirm-email')
    confirm_password = request.form.get('confirm-password')

    user = User.query.filter_by(email=email).first()

    if email != confirm_email or password != confirm_password:
        flash('Email or password do not match')
        return redirect('/register')

    elif user:
        flash('Email is already taken')
        return redirect('/register')

    else:
        flash('Successfully registered!')
        new_user = User(fname=fname,
                        lname=lname,
                        email=email,
                        password=password)

        db.session.add(new_user)
        db.session.commit()

    session['email'] = email

    return redirect(url_for('user_profile'))


@app.route('/profile')
def user_profile():
    """Display user's profile page"""

    # YOUR_API_KEY = os.environ['YOUR_API_KEY']
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    user_fname = user.fname
    created_trips = user.created_trips
    other_trips = user.trips

    return render_template('profile.html', fname=user_fname, created_trips=created_trips, other_trips=other_trips)


@app.route('/trip_name_page')
def trip_itinerary():
    pass


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app, 'trips')

    db.create_all()

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

