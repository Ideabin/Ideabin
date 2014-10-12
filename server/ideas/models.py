# Import the database object (db) from the main application module
from misc import db

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
    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False)
    title = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='')

    story = db.Column(db.Text, default='')
    vote_count = db.Column(db.Integer, default=0)

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    # Todo: Tags

    def __init__(self, title, desc, user_id):
        self.title = title
        self.desc = desc
        self.user_id = user_id

    def __repr__(self):
        return '<Idea %r>' % self.title

    def new(title, desc, user_id):
        """
        Add a new idea to the database
        """
        new_idea = Idea(title, desc, user_id)
        db.session.add(new_idea)
        db.session.commit()
        new_idea.__repr__()
        return new_idea

    def delete(self):
        """
        Remove an idea from the database
        """
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        Update an idea's data to new values.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def voting(self):
        """
        Increases the vote count.
        """
        self.vote_count += 1
        db.session.commit()
        return self

    def unvoting(self):
        """
        Decreases the vote count.
        """
        self.vote_count -= 1
        db.session.commit()
        return self

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
