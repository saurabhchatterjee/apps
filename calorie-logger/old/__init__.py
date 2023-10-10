from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_pyfile(config)
    from models import db
    db.init_app(app)

