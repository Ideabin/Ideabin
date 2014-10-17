# Import the database object (db) from the main application module
from misc import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


class Report(db.Model):
    __tablename__ = 'report'

    # report_id =
    # reported_on =
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
        Reporting on an existing idea by an existing user.
        """
        report = Report(user_id, idea_id)
        try:
            db.session.add(report)
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
