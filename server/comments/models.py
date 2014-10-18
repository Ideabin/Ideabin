# Import the database object (db) from the main application module
from misc import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


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
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, user_id, idea_id, desc_md, desc_html):
        self.user_id = user_id
        self.idea_id = idea_id
        self.desc_md = desc_md
        self.desc_html = desc_html

    def __repr__(self):
        return '<Comment %r>' % self.desc_md

    def new(title, user_id, idea_id, desc_md, desc_html):
        """
        Add a new comment to the database
        """
        new_cmnt = Comment(user_id, idea_id, desc_md, desc_html)
        db.session.add(new_cmnt)
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

    @property
    def json(self):
        """
        Return the comment's data in json form
        """
        json = {}
        for prop, val in vars(self).items():
            if not prop.startswith('_'):
                json.update({prop: str(val)})
        return json
