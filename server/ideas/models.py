from misc import db

from flask import url_for

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt

import markdown2

from server.users.models import User
from server.votes.models import Vote
from server.tags.models import Tag
from server.tagging.models import Tagging


class Idea(db.Model):
    __tablename__ = 'idea'

    idea_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False)

    title = db.Column(db.String(500), nullable=False)
    desc_md = db.Column(db.Text, nullable=False)
    desc_html = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(20), default='')

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, title, desc, user_id):
        self.title = title
        self.user_id = user_id

        self.desc_md = desc
        self.desc_html = str(markdown2.markdown(desc))

    def __repr__(self):
        return '<Idea %r>' % self.title

    def new(title, desc, user_id, tags=None):
        """
        Add a new idea to the database
        """
        new_idea = Idea(title, desc, user_id)

        # Todo: Create taggings with tagnames passed
        # The tags themselves should be created if they don't exist
        if tags:
            pass

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

    @property
    def url(self):
        return url_for('ideas.id', idea_id=self.idea_id, _external=True)

    @property
    def vote_count(self):
        return Vote.query.filter_by(idea_id=self.idea_id).count()

    @property
    def comments_url(self):
        return url_for('comments.list', idea_id=self.idea_id, _external=True)

    @property
    def user(self):
        """
        Get basic info of the user of current idea
        """
        user = User.query.filter_by(user_id=self.user_id).first()
        json = dict(
            user_id=str(user.user_id),
            username=user.username,
            created_on=user.created_on.strftime('%a, %d %b %Y %H:%M:%S')
        )
        return json

    @property
    def tags(self):
        """
        Get all tags of the idea
        """

        taggings = Tagging.query.filter_by(idea_id=self.idea_id).all()

        tags = []
        for t in taggings:
            tags.append(Tag.query.filter_by(tag_id=t.tag_id).first().tagname)

        return tags

    @property
    def json(self):
        """
        Return the idea's data in json form
        """
        json = dict(
            idea_id=str(self.idea_id),
            title=self.title,
            desc_md=self.desc_md,
            desc_html=self.desc_html,
            status=self.status,
            vote_count=self.vote_count,
            created_on=self.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
            tags=self.tags,
            url=self.url,
            comments_url=self.comments_url,
            user=self.user
        )
        return json
