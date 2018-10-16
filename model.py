from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    """Create User object"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(12), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')


    def __repr__(self):
        """Display readable user information"""

        return f"""<User: user_id {self.user_id}, 
                    name {self.fname} {self.lname}, 
                    email {self.email}>"""



class Trip(db.Model):
    """Create Trip object"""

    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    trip_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    creator = db.relationship('User', backref='created_trips')
    travel_buddies = db.relationship('User', secondary='user_trips', backref='trips')


    def __repr__(self):
        """Display readable trip information"""

        return f"""<Trip: trip_id {self.trip_id}, 
                    name {self.trip_name}, 
                    creator {self.creator_id}, 
                    duration {self.start_date} - {self.end_date}>"""

    @staticmethod
    def convert_date_format(date):

        month, day, year = date.split("/")
        return datetime.date(int(year), int(month), int(day))



class UserTrip(db.Model):
    """Create UserTrip object"""

    __tablename__ = 'user_trips'

    user_trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'), nullable=False)


    def __repr__(self):
        """Display readable information about id of user and trip"""

        return f"""<UserTrip: user_trip_id {self.user_trip_id}, 
                    user_id {self.user_id}, 
                    trip_id {self.trip_id}>"""



class Place(db.Model):
    """Create Place object"""

    __tablename__ = 'places'

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    place_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(150))

    user = db.relationship('User', backref='places')
    trip = db.relationship('Trip', backref='places')


    def __repr__(self):
        """Display readable information about the place"""

        return f"""<Place: place_id {self.place_id}, 
                    place_name {self.place_name},  
                    user {self.user_id}, 
                    trip {self.trip_id}, 
                    comment {self.comment}>"""



def connect_to_db(app, db_name):
    """Connect to database"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app, 'trips')
    print("Connected to DB.")




