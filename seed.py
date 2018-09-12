from sqlalchemy import func
from model import *
from server import app
from sqlalchemy import func
import datetime


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

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

    print("Trips")

    Trip.query.delete()

    for row in open("seed_data/u.trip"):
        row = row.rstrip()
        trip_id, creator_id, trip_name, start_date, end_date = row.split("|")

        start_date = datetime.datetime.strptime(start_date, "%d-%B-%Y")
        end_date = datetime.datetime.strptime(end_date, "%d-%B-%Y")

        trip = Trip(creator_id=creator_id,
                    trip_name=trip_name,
                    start_date=start_date,
                    end_date=end_date)

        user_trip = UserTrip(trip_id=trip_id,
                            user_id=creator_id)

        db.session.add(trip)
        db.session.add(user_trip)

    db.session.commit()


def load_places():
    """Load places from u.places into database."""

    print("Places")

    Place.query.delete()

    for row in open("seed_data/u.place"):
        row = row.rstrip()
        place_id, trip_id, user_id, place_name, comment = row.split("|")

        place = Place(trip_id=trip_id,
                    user_id=user_id,
                    place_name=place_name,
                    comment=comment)

        db.session.add(place)

    db.session.commit()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app, 'trips')

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_trips()
    # load_places()
    # set_val_user_id()
