# Import the database object (db) from the main application module
from server import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

class User(db.Model):
    id = db.Column(UUID(), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.id = uuid.uuid4()
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def new(username, email):
        new_user = User(username, email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            if str(e).index('is not unique'):
                db.session.rollback()
                print ("Not adding '%s' as it already exists." % e.params[1])
