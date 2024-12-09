from flask import Flask
from . import routes

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    # Register blueprints or routes
    app.register_blueprint(routes.bp)

    return app