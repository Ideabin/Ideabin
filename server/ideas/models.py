# Import the database object (db) from the main application module
from server import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


class Idea(db.Model):
    __tablename__ = 'idea'

    idea_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID())
    title = db.Column(db.String(120))
    desc = db.Column(db.String(300), default='')
    # status = db.Column(db.String(20), default='')

    # story = db.Column(db.String(120), default='')
    # langs = db.Column(db.String(120), default='')
    vote_count = db.Column(db.Integer, default=0)

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(db.DateTime, default=dt.datetime.utcnow())

    # TODO: Tags

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

    def __repr__(self):
        return '<Idea %r>' % self.title

    def new(title, user_id):
        """
        Add a new idea to the database
        """
        new_idea = Idea(title, user_id)
        try:
            db.session.add(new_idea)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()

    def delete(self):
        """
        Remove an idea from the database
        """
        db.session.delete(self)
        db.session.commit()
        # return self

    def update(self, **kwargs):
        """
        Update an idea's data to new values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    @property
    def json(self):
        """
        Return the idea's data in json form
        """
        json = {}
        for prop, val in vars(self).items():
            if not prop.startswith('_'):
                json.update({prop: str(val)})
        return json
