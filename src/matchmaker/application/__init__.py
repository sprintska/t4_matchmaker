import os

from flask import Flask


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_prefixed_env(prefix="MATCHMAKER_")
    app.config["HASURA_URL"] = os.environ.get("MATCHMAKER_HASURA_URL")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import routes

        return app
