from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid


class Tagging(db.Model):
    __tablename__ = 'tagging'

    tag_id = db.Column(
        UUID(), db.ForeignKey('tag.tag_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)
    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False, primary_key=True)

    def __init__(self, tag_id, idea_id):
        self.tag_id = tag_id
        self.idea_id = idea_id

    def __repr__(self):
        return '<Tagging %r>' % self.tag_id

    def new(tag_id, idea_id):
        """
        Add a new tag to an existing idea
        """
        new_tag = Tagging(tag_id, idea_id)
        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLexc.IntegrityError as e:
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
