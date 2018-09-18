from sqlalchemy import func
from model import *
from server import app
from sqlalchemy import func
from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, fname, lname, email, password = row.split("|")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password)

        db.session.add(user)

    db.session.commit()


def load_trips():
    """Load trips from u.trips into database."""

    for row in open("seed_data/u.trip"):
        row = row.rstrip()
        trip_id, creator_id, trip_name, start_date, end_date = row.split("|")

        start_date = datetime.strptime(start_date, "%d-%B-%Y")
        end_date = datetime.strptime(end_date, "%d-%B-%Y")

        trip = Trip(creator_id=creator_id,
                    trip_name=trip_name,
                    start_date=start_date,
                    end_date=end_date)

        db.session.add(trip)

    db.session.commit()


def load_places():
    """Load places from u.places into database."""

    for row in open("seed_data/u.place"):
        row = row.rstrip()
        place_id, trip_id, user_id, place_name, comment = row.split("|")

        place = Place(trip_id=trip_id,
                    user_id=user_id,
                    place_name=place_name,
                    comment=comment)

        db.session.add(place)

    db.session.commit()


def load_user_trips():
    """Associate users to trips from u.user_trips into database."""

    for row in open("seed_data/u.user_trips"):
        row = row.rstrip()
        user_trip_id, user_id, trip_id = row.split("|")

        user_trip = UserTrip(user_id=user_id,
                            trip_id=trip_id)

        db.session.add(user_trip)

    db.session.commit()


def del_data_in_tables():
    """Delete data from all tables in the database to avoid adding duplicates"""

    Place.query.delete()
    Trip.query.delete()
    User.query.delete()
    UserTrip.query.delete()


if __name__ == "__main__":
    connect_to_db(app, 'trips')

    # In case tables haven't been created, create them
    db.create_all()

    # del_data_in_tables()
    load_users()
    load_trips()
    load_places()
    load_user_trips()

