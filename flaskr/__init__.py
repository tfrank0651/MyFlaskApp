import os
from flask import Flask
from . import db
from . import auth
from . import blog


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello world!'

    # initialize the database
    db.init_app(app)
    # Register then blueprint for auth
    app.register_blueprint(auth.bp)
    # Register the blueprint for blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
