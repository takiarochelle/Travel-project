from sqlalchemy import func
from model import *
from server import app


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

        start_date = datetime.datetime.strptime(start_date, "%d-%b-%Y")
        end_date = datetime.datetime.strptime(end_date, "%d-%b-%Y")

        trip = Trip(creator_id=creator_id,
                    trip_name=trip_name,
                    start_date=start_date,
                    end_date=end_date)

        db.session.add(trip)

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



if __name__ == "__main__":
    connect_to_db(app, 'trips')

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    # load_trips()
    # load_places()
    # set_val_user_id()
