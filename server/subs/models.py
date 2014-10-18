# Import the database object (db) from the main application module
from misc import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


class TSub(db.Model):
    __tablename__ = 'tsub'

    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE', ),
        nullable=False, primary_key=True, )
    tag_id = db.Column(
        UUID(), db.ForeignKey('tag.tag_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    subscribed_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, user_id, tag_id):
        self.user_id = user_id
        self.tag_id = tag_id

    def new(user_id, tag_id):
        """
        Subscribing to an existing tag by an existing user.
        """
        sub = TSub(user_id, tag_id)
        try:
            db.session.add(sub)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: (i)Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()
        return True

    def delete(self):
        """
        Deletes the subscription
        """
        db.session.delete(self)
        db.session.commit()
        return True


class USub(db.Model):
    __tablename__ = 'usub'

    sub_to = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE', ),
        nullable=False, primary_key=True, )
    sub_by = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    subscribed_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, sub_to, sub_by):
        self.sub_to = sub_to
        self.sub_by = sub_by

    def new(sub_to, sub_by):
        """
        Subscribing to an existing user by an existing user.
        """
        sub = USub(sub_to, sub_by)
        try:
            db.session.add(sub)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: (i)Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()
        return True

    def delete(self):
        """
        Deletes the subscription
        """
        db.session.delete(self)
        db.session.commit()
        return True


class ISub(db.Model):
    __tablename__ = 'isub'

    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE', ),
        nullable=False, primary_key=True, )
    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    subscribed_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, user_id, idea_id):
        self.user_id = user_id
        self.idea_id = idea_id

    def new(user_id, idea_id):
        """
        Subscribing to an existing idea by an existing user.
        """
        sub = ISub(user_id, idea_id)
        try:
            db.session.add(sub)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: (i)Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()
        return True

    def delete(self):
        """
        Deletes the subscription
        """
        db.session.delete(self)
        db.session.commit()
        return True
