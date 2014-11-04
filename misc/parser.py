import re
from urllib.parse import urlparse

from flask import request
from misc import validate_uuid

from server.exceptions import MissingDataError, ParserError


class Parser(object):

    @classmethod
    def get_dict(cls, src):
        if src == 'uri':
            return request.args
        elif src == 'form':
            return request.form
        elif src == 'json':
            return request.json

    @classmethod
    def get_key(cls, src, key):
        _dict = cls.get_dict(src)
        _k = _dict.get(key)
        return _k

    @classmethod
    def anything(cls, key, src='json', optional=False):
        _e = cls.get_key(src, key)
        if not _e:
            if optional:
                return None
            else:
                raise MissingDataError(key)
        return _e

    @classmethod
    def bool(cls, key, src='json', optional=False):
        _b = cls.get_key(src, key)
        if _b is None:
            if optional:
                return None
            else:
                raise MissingDataError(key)
        if isinstance(_b, bool) is False:
            raise ParserError(key, 'Is not bool')
        return _b

    @classmethod
    def string(cls, key, src='json', min=None, max=None,
               valid_values=None, optional=False):
        _s = cls.get_key(src, key)
        if _s is None:
            if optional:
                return None
            else:
                raise MissingDataError(key)

        # Note: Do we have a problem with numbers?
        if _s.isdigit():
            raise ParserError(key, 'Can not be a number')

        _s_len = len(_s)
        if max is not None and _s_len > max:
            raise ParserError(key, 'Too long (max=%d)' % max)
        if min is not None and _s_len < min:
            raise ParserError(key, 'Too short (min=%d)' % min)
        if valid_values is not None and _s not in valid_values:
            raise ParserError(key, 'Is not valid')
        return _s

    @classmethod
    def int(cls, key, src='json', min=None, max=None, optional=False):
        _i = cls.get_key(src, key)
        if _i is None:
            if optional:
                return None
            else:
                raise MissingDataError(key)
        if _i.isdigit() is False:
            raise ParserError(key, 'NaN')
        else:
            _i = int(_i)
        if max is not None and _i > max:
            raise ParserError(key, 'Too large (max=%d)' % max)
        if min is not None and _i < min:
            raise ParserError(key, 'Too small (min=%d)' % min)
        return _i

    @classmethod
    def uuid(cls, key, src='json', optional=False):
        _u = cls.get_key(src, key)
        if _u is None:
            if optional:
                return None
            else:
                raise MissingDataError(key)
        if not validate_uuid(_u):
            raise ParserError(key, 'Not a valid UUID')
        return _u

    @classmethod
    def uri(cls, key, src='json', optional=False):
        _u = cls.get_key(src, key)
        if _u is None:
            if optional:
                return None
            else:
                raise MissingDataError(key)
        d = urlparse(_u)
        if d.scheme not in ['http', 'https'] or not d.netloc:
            raise ParserError(key, 'Not a valid URI')
        return _u

    @classmethod
    def email(cls, key, src='json', optional=False):
        _e = cls.get_key(src, key)
        if not _e:
            if optional:
                return None
            else:
                raise MissingDataError(key)
        if not re.match("[^@]+@[^@]+\.[^@]+", _e):
            raise ParserError(key, 'Not a valid email address')
        return _e

    @classmethod
    def list(cls, key, src='json', elements=None, optional=False):
        """
        Checks if the key is a comma separated list.
        """
        _l = cls.get_key(src, key)
        if not _l:
            if optional:
                return None
            else:
                raise MissingDataError(key)

        _l = _l.strip().split(",")

        # Each tag should be in range
        for e in _l:
            if len(e) < 2 or len(e) > 50:
                raise ParserError(key, 'Contains illegal value `%s`' % e)

        if elements is not None:
            for e in _l:
                if e not in elements:
                    raise ParserError(key, 'Contains illegal value `%s`' % e)
        return _l
