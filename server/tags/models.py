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
    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False)
    tagname = db.Column(db.String(500), nullable=False)

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, tagname, idea_id):
        self.title = tagname
        self.idea_id = idea_id

    def __repr__(self):
        return '<Tag %r>' % self.tagname

    def new(tagname, idea_id):
        """
        Add a new tag to the database
        """
        new_tag = Tag(tagname, idea_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: (i)Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()

        new_tag.__repr__()

        return new_tag

    def delete(self):
        """
        Remove a tag from the database
        """
        db.session.delete(self)
        db.session.commit()
        return self

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
