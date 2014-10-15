from flask import Flask


def create_app():
    app = Flask(__name__)

    # Configurations
    app.config.from_object('config')
    app.config.from_pyfile('secrets', silent=True)

    # Error handling
    import server.errors
    errors.init_error_handlers(app)

    # A uuid url converter for flask
    from misc.flask_uuid import FlaskUUID
    FlaskUUID(app)

    from misc import db
    db.init_app(app)

    # Login Manager
    import server.login
    server.login.login_manager.init_app(app)

    # Blueprints
    from server.views import api_bp
    from server.users.views import users_bp
    from server.ideas.views import ideas_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(ideas_bp, url_prefix='/ideas')

    return app
