from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration files
    app.config.from_object('config')
    app.config.from_object('secrets')

    from misc import db
    db.init_app(app)

    # Login Manager
    import frontend.login
    frontend.login.login_manager.init_app(app)

    # Blueprints
    from frontend.views import frontend_bp
    from frontend.login.views import login_bp
    from frontend.login.views import logout_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(logout_bp, url_prefix='/logout')

    return app
