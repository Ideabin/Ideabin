# Import the database object (db) from the main application module
from misc import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


class Vote(db.Model):
    __tablename__ = 'vote'

    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE', ),
        nullable=False, primary_key=True, )
    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    def __init__(self, user_id, idea_id):
        self.user_id = user_id
        self.idea_id = idea_id

    def new(user_id, idea_id):
        """
        Add a new vote by an user on an existing idea
        """
        new_user = Vote(user_id, idea_id)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: (i)Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()
        return True

    def delete(self):
        """
        Remove a tag from the database
        """
        db.session.delete(self)
        db.session.commit()
        return True
