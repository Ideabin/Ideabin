from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt

from server.users.models import User
from server.ideas.models import Idea
from server.comments.models import Comment


class NotifCommentByUser(db.Model):
    __tablename__ = 'notif_comment_by_user'

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

    comment_id = db.Column(
        UUID(), db.ForeignKey('comment.comment_id', ondelete='CASCADE'),
        nullable=False)

    # Todo: Add proper Read/Unread support
    read = db.Column(db.Boolean, nullable=False, server_default='0')

    created_on = db.Column(
        db.DateTime, default=dt.datetime.utcnow, nullable=False)

    def __init__(self, user_by, user_to, idea_id, comment_id):
        self.user_by = user_by
        self.user_to = user_to
        self.idea_id = idea_id
        self.comment_id = comment_id

    def __repr__(self):
        return '<Notif Comment by User: %r>' % self.notif_id

    def new(user_by, user_to, idea_id, comment_id):
        """
        Add a new notif to the database
        """
        notif = NotifCommentByUser(user_by, user_to, idea_id, comment_id)
        db.session.add(notif)
        db.session.commit()

        notif.__repr__()
        return notif

    @property
    def idea(self):
        return Idea.get(idea_id=self.idea_id)

    @property
    def comment(self):
        return Comment.get(comment_id=self.comment_id)

    @property
    def title(self):
        username = User.get(user_id=self.user_by).username
        return "%s commented on the idea \"%s\"." % (username, self.idea.title)

    @property
    def json(self):
        json = dict(
            id=str(self.notif_id),
            by=User.get(user_id=self.user_by).basic,
            to=User.get(user_id=self.user_to).basic,
            title=self.title,
            link=self.idea.url,
            object=self.comment.basic,
            created_on=self.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
        )
        return json
