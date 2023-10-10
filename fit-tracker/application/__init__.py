from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """
    Initialize the core application.
    we're creating our Flask app object and
    stating that it should be configured using
    a class called Config in a file named config.py
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Import parts of our application
        from . import routes

        db.create_all()

        return app
