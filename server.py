import os
from flask import Flask, redirect, request, render_template, session, url_for, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import User, Trip, Place, UserTrip, connect_to_db, db
import config

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
YOUR_API_KEY = config.YOUR_API_KEY


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
        return redirect(url_for('user_profile', username=valid_user.username))

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
    username = request.form.get('reg-username')

    user_by_email = User.query.filter_by(email=email).first()
    user_by_username = User.query.filter_by(username=username).first()

    if email != confirm_email or password != confirm_password:
        flash('Email or password do not match')
        return redirect('/register')

    elif user_by_email or user_by_username:
        flash('Email or username is already taken')
        return redirect('/register')

    else:
        flash('Successfully registered!')
        new_user = User(fname=fname,
                        lname=lname,
                        email=email,
                        password=password,
                        username=username)

        db.session.add(new_user)
        db.session.commit()

    session['email'] = email

    return redirect(url_for('user_profile', username=username))


@app.route('/profile/<username>')
def user_profile(username):
    """Display user's profile page"""

    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    user_fname = user.fname
    created_trips = user.created_trips
    other_trips = user.trips
    profile_image = user.image_file

    return render_template('profile.html',
                            fname=user_fname, 
                            created_trips=created_trips, 
                            other_trips=other_trips, 
                            username=username,
                            profile_image=profile_image)


# @app.route('/my_submit', methods=['POST'])
# def handle_submit():
#     """Save profile image"""

#     f = request.files['my_photo']
#     filename = f.save('static/' + f.filename)

#     email = session.get('email')
#     user = User.query.filter_by(email=email).first()

#     user.image_file = filename

#     db.session.commit()

#     return redirect(url_for('user_profile', 
#                             fname=user.fname, 
#                             created_trips=user.created_trips, 
#                             other_trips=user.trips, 
#                             profile_image=user.image_file))


@app.route('/add-trip')
def add_trip():
    """Add trip to users list of trips in the database"""

    return render_template('add_trip.html')


@app.route('/validate-trip', methods=['POST'])
def validate_trip():

    user = User.query.filter_by(email=session['email']).first()

    trip_name = request.form.get('trip-name')
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date')

    start_date = Trip.convert_date_format(start_date)
    end_date = Trip.convert_date_format(end_date)

    new_trip = Trip(creator_id=user.user_id,
                    trip_name=trip_name,
                    start_date=start_date,
                    end_date=end_date)

    db.session.add(new_trip)

    db.session.commit()

    places = new_trip.places
    travel_buddies = new_trip.travel_buddies

    return redirect(url_for('trip_itinerary',
                            YOUR_API_KEY=YOUR_API_KEY,
                            trip_id=new_trip.trip_id,
                            trip_name=trip_name, 
                            start_date=start_date,
                            end_date=end_date,
                            places=places,
                            travel_buddies=travel_buddies))


@app.route('/<trip_name>-<trip_id>')
def trip_itinerary(trip_name, trip_id):
    
    email = session.get('email')
    place = request.args.get('place-name')
    user = User.query.filter_by(email=email).first()
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    place_exist = Place.query.filter_by(trip_id=trip_id, place_name=place).first()

    if place and place_exist == None:
        new_place = Place(trip_id=trip_id,
                        user_id=user.user_id,
                        place_name=place)

        db.session.add(new_place)
        db.session.commit()

    places = trip.places
    travel_buddies = trip.travel_buddies

    return render_template('itinerary.html',
                            YOUR_API_KEY=YOUR_API_KEY, 
                            trip_name=trip_name, 
                            trip_id=trip_id,
                            start_date=trip.start_date,
                            end_date=trip.end_date,
                            places=places,
                            travel_buddies=travel_buddies)



@app.route('/logout')
def logout():
    """Display logout page"""

    session.clear()

    return render_template('logout.html')


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app, 'trips')

    db.create_all()

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

