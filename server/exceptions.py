class IdeaBinError(Exception):
    """ Base class for app exceptions. """
    pass


class BaseError(IdeaBinError):
    def __init__(self, msg=None, status=400):
        self.msg = msg
        self.status = status


class InvalidRequest(BaseError):
    def __init__(self, msg='The input data sent should be json.'):
        super(InvalidRequest, self).__init__(
            msg=msg,
            status=400
        )


class Unauthorized(BaseError):
    def __init__(self, msg=''):
        super(Unauthorized, self).__init__(
            msg='You need to be logged in to access this URL.',
            status=401
        )


class NotFound(BaseError):
    def __init__(self, msg='Not Found'):
        super(NotFound, self).__init__(
            msg=msg,
            status=404
        )


class NotAllowed(BaseError):
    def __init__(self, msg=''):
        super(NotAllowed, self).__init__(
            msg='This method is not allowed for the following resource.',
            status=405
        )


class Conflict(BaseError):
    def __init__(self, msg='A conflict occurred while processing the data.'):
        super(Conflict, self).__init__(
            msg=msg,
            status=409
        )


class ServerError(BaseError):
    def __init__(self, msg=''):
        super(ServerError, self).__init__(
            msg='The server encountered an unexpected condition that '
                'prevented it from fulfilling the request.',
            status=500
        )


class ParserError(IdeaBinError):
    def __init__(self, key, desc):
        self.key = key
        self.desc = desc


class MissingDataError(ParserError):
    def __init__(self, key):
        super(MissingDataError, self).__init__(
            key=key,
            desc='Missing')
