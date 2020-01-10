import os
from flask import Flask

# Application factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping (
        SECRET_KEY = "dev"
        # No database :)
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import line_broadcaster
    app.register_blueprint(line_broadcaster.bp)

    @app.route("/hello")
    def hello():
        line_broadcaster.broadcastMessage()
        return "Hello, World!"

    @app.route("/")
    def homepage():
        return "HP"

    return app
