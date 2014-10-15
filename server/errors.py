from .exceptions import *

from flask import (
    make_response,
    jsonify,
    request
)


def init_error_handlers(app):

    @app.errorhandler(BaseError)
    def base_error_handler(error):
        return make_response(
            jsonify(
                documentation_url='http://ideabin.readthedocs.org/',
                message=error.msg,
                status=error.status
            ),
            error.status
        )

    @app.errorhandler(404)
    def not_found_handler(error):
        return base_error_handler(
            NotFound()
        )

    @app.errorhandler(401)
    def not_found_handler(error):
        return base_error_handler(
            Unauthorized()
        )

    @app.errorhandler(500)
    def exception_handler(error):
        return base_error_handler(
            ServerError()
        )
