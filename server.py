import os
from flask import Flask, redirect, request, render_template, session, url_for, flash, jsonify
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

    email = session.get('email')
    user = User.query.filter_by(email=email).first()

    return render_template('index.html', user=user)


@app.route('/validate-login', methods=['POST'])
def validate_login():
    """Check that user entered correct email and password."""

    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        session['email'] = email
        return redirect(url_for('user_profile', username=user.username))

    else:
        flash('Email or password is incorrect')


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

    elif user_by_email or user_by_username:
        flash('Email or username is already taken')

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

    if session:

        user = User.query.filter_by(username=username).first()

        return render_template('profile.html', 
                                user=user)


@app.route('/my_submit', methods=['POST'])
def handle_submit():
    """Save profile image"""

    f = request.files['my_photo']
    f.save('static/' + f.filename)

    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    user.image_file = 'static/' + f.filename

    db.session.commit()

    return redirect(url_for('user_profile', username=user.username))


@app.route('/<trip_name>-<trip_id>')
def trip_itinerary(trip_name, trip_id):
    """Display page with itinerary for the trip"""
    
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    users = User.query.filter(User.email!=email).all()
    trip = Trip.query.filter_by(trip_id=trip_id).first()

    return render_template('itinerary.html',
                            trip_name=trip_name,
                            trip_id=trip_id,
                            trip=trip,
                            username=user.username,
                            users=users)


@app.route('/validate-trip', methods=['POST'])
def validate_trip():
    """Allow user to create a new trip"""

    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    trip_name = request.form.get('trip-name')
    start_date = request.form.get('start-date')
    end_date = request.form.get('end-date')

    new_trip = Trip(creator_id=user.user_id,
                    trip_name=trip_name,
                    start_date=start_date,
                    end_date=end_date)

    db.session.add(new_trip)

    db.session.commit()

    return redirect(url_for('trip_itinerary',
                            trip_name=new_trip.trip_name, 
                            trip_id=new_trip.trip_id))


@app.route('/add-friends.json')
def add_friends():
    """Display list of users"""
    
    user_id = int(request.args.get('user_id'))
    trip_id = int(request.args.get('trip_id'))
    user = User.query.filter_by(user_id=user_id).first()
    trip = Trip.query.filter_by(trip_id=trip_id).first()

    trip.travel_buddies.append(user)

    db.session.commit()

    return jsonify({'profile_img': user.image_file,
                    'full_name': f'{user.fname} {user.lname}'})


@app.route('/add-place/<trip_id>')
def add_place(trip_id):
    """Add place to a trip itinerary"""

    trip = Trip.query.filter_by(trip_id=trip_id).first()
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    place_name = request.args.get('place-location')
    place_exists = Place.query.filter_by(trip_id=trip_id, place_name=place_name).first()

    if place_name and place_exists == None:
        new_place = Place(trip_id=trip_id,
                        user_id=user.user_id,
                        place_name=place_name)

        db.session.add(new_place)
        db.session.commit()

    return redirect(url_for('trip_itinerary',
                            trip_name=trip.trip_name,
                            trip_id=trip_id))


@app.route('/delete-place.json')
def delete_place():
    """Remove place from the trip"""

    place_id = int(request.args.get('place_id'))
    Place.query.filter_by(place_id=place_id).delete()
    db.session.commit()

    return jsonify({ 'place_id': place_id })


@app.route('/delete-trip.json', methods=['POST'])
def delete_trip():
    """Remove trip from users list of trips"""

    trip_id = int(request.form.get('trip_id'))
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    user = User.query.filter_by(email=session.get('email')).first()

    if user == trip.creator:
        Trip.query.filter_by(trip_id=trip_id).delete()

    else:
        trip.travel_buddies.remove(user)
        
    db.session.commit()

    return jsonify({ 'trip_id': trip_id })


@app.route('/add-comment/<place_id>.json', methods=['POST'])
def add_comment(place_id):
    """Lets user add a comment to a place on the Trip"""

    comment = request.form.get('place-comment')
    place = Place.query.filter_by(place_id=place_id).first()
    trip_id = place.trip_id
    trip = Trip.query.filter_by(trip_id=trip_id).first()
    place.comment = comment 
    db.session.commit()

    return jsonify({ 'comment': place.comment })


@app.route('/logout')
def logout():
    """Redirect to Homepage"""

    session.clear()

    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app, 'trips')

    db.create_all()

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")

