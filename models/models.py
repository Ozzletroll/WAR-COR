from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Basic user data
    username = db.Column(db.String(30))
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))

    # Database relationships

    # campaigns =
    # comments =


class Campaign(db.Model):
    __tablename__ = "campaigns"

    id = db.Column(db.Integer, primary_key=True)

    # Basic campaign data
    title = db.Column(db.String(250))

    # Database relationships

    # participants =
    # events =
    # comments =


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)


class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)