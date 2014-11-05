from misc import db

from flask import url_for

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt

from server.tagging.models import Tagging
from server.subscriptions.models import TagSub


class Tag(db.Model):
    __tablename__ = 'tag'

    tag_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    tagname = db.Column(db.String(50), unique=True, nullable=False)

    desc = db.Column(db.Text(), default='')
    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow, nullable=False)

    def __init__(self, tagname, desc):
        self.tagname = tagname.strip()
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
        Update a tag's data to new values.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    @property
    def subscribers(self):
        """
        Users who have subscribed
        """

        tags = TagSub.query.filter_by(sub_to=self.tag_id).all()

        return [str(i.sub_by) for i in tags]

    @property
    def url(self):
        return url_for('tags.id', tag_id=self.tag_id, _external=True)

    @property
    def ideas(self):
        """
        Get all ideas of the tag
        """

        taggings = Tagging.query.filter_by(tag_id=self.tag_id).all()

        return [str(t.idea_id) for t in taggings]

    # Todo: Renaming to a new (or existing?) one

    @property
    def json(self):
        """
        Return the tag's data in json form
        """
        json = dict(
            tag_id=str(self.tag_id),
            tagname=self.tagname,
            desc=self.desc,
            created_on=self.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
            ideas=self.ideas,
            subscribers=self.subscribers,
            url=self.url
        )
        return json
