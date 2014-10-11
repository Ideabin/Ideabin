from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration files
    app.config.from_object('config')

    # Blueprints
    from frontend.views import index_bp

    app.register_blueprint(index_bp)

    return app
