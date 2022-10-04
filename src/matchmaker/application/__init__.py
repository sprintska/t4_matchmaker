import os

from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",  # CHANGE ME
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import routes

        return app
