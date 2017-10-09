import os
import settings
import errors
from flask import Flask, Blueprint
from database import db
from config import *
from flask_marshmallow import Marshmallow


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(config or {})
    app.config.from_envvar('FLASK_SETTINGS', silent=True)
    app.config.from_object(os.environ['FLASK_CONFIG'])

    from apis import blueprint as api

    app.register_blueprint(api)
    register_teardowns(app)

    return app


def register_teardowns(flask_app):
    db.close_db_factory(flask_app)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

