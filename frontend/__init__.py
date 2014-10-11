from flask import Flask

import os

frontend_folder = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(frontend_folder, 'templates')
static_folder = os.path.join(frontend_folder, 'static')

def create_app():
    app = Flask(__name__,
                static_folder=static_folder,
                template_folder=template_folder)

    app.debug = True

    # Configuration files
    app.config.from_object('config')

    # Blueprints
    from frontend.views import index_bp

    app.register_blueprint(index_bp)

    return app
