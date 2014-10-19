# Import the database object (db) from the main application module
from misc import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt

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
    vote_count = db.Column(db.Integer, default=0)

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, title, desc, user_id):
        self.title = title
        self.user_id = user_id

        # Todo: Use a markdown converter to convert the md to html
        self.desc_md = desc
        self.desc_html = desc

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
        json = {}

        for prop, val in vars(self).items():
            if not prop.startswith('_'):
                json.update({prop: str(val)})

        json.update({"tags": self.tags})
        return json
