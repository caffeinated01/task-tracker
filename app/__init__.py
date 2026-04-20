import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('app.config.Config')

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    from . import db
    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    return app
