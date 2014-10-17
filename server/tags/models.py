# Import the database object (db) from the main application module
from misc import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


class Tag(db.Model):
    __tablename__ = 'tag'

    tag_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    tagname = db.Column(db.String(500), nullable=False)

    desc = db.Column(db.Text(), default='')
    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, tagname, desc):
        self.tagname = tagname
        self.desc = desc

    def __repr__(self):
        return '<Tag %r>' % self.tagname

    def new(tagname, desc=''):
        """
        Add a new tag to the database
        """
        new_tag = Tag(tagname, desc)
        db.session.add(new_tag)
        db.session.commit()

        new_tag.__repr__()
        return new_tag

    def delete(self):
        """
        Remove a tag from the database
        """
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        Update an tag's data to new values.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    # todo: renaming to a new one or renaming to an existing one.
    # def rename(self):
    #     return 0

    @property
    def json(self):
        """
        Return the tag's data in json form
        """
        json = {}
        for prop, val in vars(self).items():
            if not prop.startswith('_'):
                json.update({prop: str(val)})
        return json
