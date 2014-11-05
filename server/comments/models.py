from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt

import markdown2

from server.users.models import User


class Comment(db.Model):
    __tablename__ = 'comment'

    comment_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False)
    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False)

    desc_md = db.Column(db.Text, nullable=False)
    desc_html = db.Column(db.Text, nullable=False)

    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow, nullable=False)

    def __init__(self, user_id, idea_id, desc):
        self.user_id = user_id
        self.idea_id = idea_id

        self.desc_md = desc
        self.desc_html = str(markdown2.markdown(desc))

    def __repr__(self):
        return '<Comment %r>' % self.desc_md

    def new(user_id, idea_id, desc):
        """
        Add a new comment to the database
        """
        new_cmnt = Comment(user_id, idea_id, desc)
        db.session.add(new_cmnt)
        db.session.commit()
        new_cmnt.__repr__()
        return new_cmnt

    def delete(self):
        """
        Remove a comment from the database
        """
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        Update a comments's data
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    @property
    def user(self):
        """
        Get basic info of the user who created comment
        """
        user = User.query.filter_by(user_id=self.user_id).first()
        json = dict(
            user_id=str(user.user_id),
            username=user.username,
            created_on=user.created_on.strftime('%a, %d %b %Y %H:%M:%S')
        )
        return json

    @property
    def json(self):
        """
        Return the comment's data in json form
        """
        json = dict(
            comment_id=str(self.comment_id),
            desc_md=self.desc_md,
            desc_html=self.desc_html,
            created_on=self.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
            user=self.user
        )
        return json
