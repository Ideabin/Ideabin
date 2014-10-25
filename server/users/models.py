from misc import db

from sqlalchemy import exc as SQLexc

from misc.uuid import UUID
import uuid

import datetime as dt

from hashlib import md5

from flask import url_for

from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(180), nullable=False)
    first_name = db.Column(db.String(120), default='')
    last_name = db.Column(db.String(120), default='')

    # Note: This data is entirely optional
    blog_url = db.Column(db.String(120), default='')
    profile_fb = db.Column(db.String(120), default='')
    profile_twitter = db.Column(db.String(120), default='')

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(db.DateTime, default=dt.datetime.utcnow())
    last_login_on = db.Column(db.DateTime, default=dt.datetime.utcnow())

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    def new(username, password, email):
        """
        Add a new user to the database
        """
        new_user = User(username, password, email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: Raise a proper exception that the view will catch
            # raise(e)
            db.session.rollback()

        new_user.__repr__()
        return new_user

    def delete(self):
        """
        Remove a user from the database
        """
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        Update a user's data to new values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    @property
    def avatar(self):
        """
        Return the url for user's gravatar image
        """
        return 'https://www.gravatar.com/avatar/%s?d=mm&s=%d' \
            % (md5(self.email.encode('utf-8')).hexdigest(), 128)

    @property
    def url(self):
        """
        Get the url for current user
        """
        return url_for('users.id', uid=self.user_id, _external=True)

    @property
    def json(self):
        """
        Return the user's data in json form
        """
        json = dict(
            user_id=str(self.user_id),
            username=self.username,
            avatar=self.avatar,
            url=self.url,
            first_name=self.first_name,
            last_name=self.last_name,
            created_on=self.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
            blog_url=self.blog_url,
            profile_fb=self.profile_fb,
            profile_twitter=self.profile_twitter
        )
        return json

    def get_id(self):
        return str(self.user_id)
