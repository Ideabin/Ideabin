from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt


class Report(db.Model):
    __tablename__ = 'report'

    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    reported_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, user_id, idea_id):
        self.user_id = user_id
        self.idea_id = idea_id

    def new(user_id, idea_id):
        """
        Report an idea
        """
        report = Report(user_id, idea_id)
        try:
            db.session.add(report)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            db.session.rollback()
        return True

    def delete(self):
        """
        Remove a tag from the database
        """
        db.session.delete(self)
        db.session.commit()
        return True
