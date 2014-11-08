from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt

from server.users.models import User


class NotifIdeaByUser(db.Model):
    __tablename__ = 'notif_idea_by_user'

    notif_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)

    user_by = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False)

    user_to = db.Column(
        UUID(), db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False)

    idea_id = db.Column(
        UUID(), db.ForeignKey('idea.idea_id', ondelete='CASCADE'),
        nullable=False)

    # Todo: Add proper Read/Unread support
    read = db.Column(db.Boolean, default=False)

    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow(), nullable=False)

    def __init__(self, user_by, user_to, idea_id):
        self.user_by = user_by
        self.user_to = user_to
        self.idea_id = idea_id

    def __repr__(self):
        return '<Notification %r>' % self.user_id

    def new(user_by, user_to, idea_id):
        """
        Add a new notif to the database
        """
        notif = Notification(user_by, user_to, idea_id)
        db.session.add(notif)
        db.session.commit()

        notif.__repr__()
        return notif

    @property
    def idea(self):
        return Idea.get(idea_id=self.idea_id)

    @property
    def message(self):
        username = User.get(user_id=self.user_by).username
        return "%s added a new idea \"%s\"." % (username, self.idea.title)

    @property
    def json(self):
        json = dict(
            id=self.notif_id,
            by=User.get(user_id=self.user_by).basic,
            to=User.get(user_id=self.user_to).basic,
            message=self.message
            link=self.idea.url,
            object=self.idea.basic,
            created_on=self.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
        )
        return json
