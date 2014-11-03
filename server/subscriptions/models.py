from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt


class TagSub(db.Model):
    __tablename__ = 'tag_sub'

    sub_by = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    sub_to = db.Column(
        UUID(), db.ForeignKey('tag.tag_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    def __init__(self, sub_by, sub_to):
        self.sub_by = sub_by
        self.sub_to = sub_to

    def new(sub_by, sub_to):
        """
        Create a new subscription
        """
        sub = TagSub(sub_by, sub_to)
        try:
            db.session.add(sub)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            db.session.rollback()
        return True

    def delete(self):
        """
        Deletes the subscription
        """
        db.session.delete(self)
        db.session.commit()
        return True


class UserSub(db.Model):
    __tablename__ = 'user_sub'

    sub_by = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    sub_to = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    def __init__(self, sub_by, sub_to):
        self.sub_by = sub_by
        self.sub_to = sub_to

    def new(sub_by, sub_to):
        """
        Create a new subscription
        """
        sub = UserSub(sub_by, sub_to)
        try:
            db.session.add(sub)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            db.session.rollback()
        return True

    def delete(self):
        """
        Deletes the subscription
        """
        db.session.delete(self)
        db.session.commit()
        return True


class IdeaSub(db.Model):
    __tablename__ = 'idea_sub'

    sub_by = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    sub_to = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    def __init__(self, sub_by, sub_to):
        self.sub_by = sub_by
        self.sub_to = sub_to

    def new(sub_by, sub_to):
        """
        Create a new subscription
        """
        sub = IdeaSub(sub_by, sub_to)
        try:
            db.session.add(sub)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            db.session.rollback()
        return True

    def delete(self):
        """
        Deletes the subscription
        """
        db.session.delete(self)
        db.session.commit()
        return True
