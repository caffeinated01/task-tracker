import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('app.config.Config')

    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    import app.db as db
    db.init_app(app)

    # Register blueprints
    from app.api import auth, board, task
    import app.views as views
    app.register_blueprint(auth.bp)
    app.register_blueprint(board.bp)
    app.register_blueprint(task.bp)
    app.register_blueprint(views.bp)

    return app
