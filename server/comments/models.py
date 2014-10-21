from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt


class Comments(db.Model):
    __tablename__ = 'comments'

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

    def __init__(self, user_id, idea_id, desc):
        self.user_id = user_id
        self.idea_id = idea_id

        # Todo: Use a markdown converter to convert the md to html
        self.desc_md = desc
        self.desc_html = desc

    def __repr__(self):
        return '<Comment %r>' % self.desc_md

    def new(title, user_id, idea_id, desc):
        """
        Add a new comment to the database
        """
        new_cmnt = Comment(user_id, idea_id, desc)
        db.session.add(new_cmnt)
        db.session.commit()
        new_idea.__repr__()
        return new_idea

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
    def json(self):
        """
        Return the comment's data in json form
        """
        json = {}
        for prop, val in vars(self).items():
            if not prop.startswith('_'):
                json.update({prop: str(val)})
        return json
