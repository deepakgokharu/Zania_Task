import os
# import getpass
from flask import Flask

from .utils.global_variables import (
    MAX_CONTENT_LENGTH, OPENAI_API_KEY
)
from .register_blueprints import register_blueprint


def create_app(test_config=None):
    """Setting env variables for openai llm model"""
    os.environ["COHERE_API_KEY"] = OPENAI_API_KEY

    """Creating and configuring an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    app.config.from_mapping(
        SECRET_KEY = 'dev', 
        MAX_CONTENT_LENGTH = (10 * MAX_CONTENT_LENGTH) # limiting the size of file for 16 megabytes, if greater than this, we will need to create other logic for uploading file
    )

    if test_config is None:
        # loading the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # loading the test config if it is passed
        app.config.from_mapping(test_config)
    
    # ensuring the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page taht says hello
    @app.route("/hello")
    def hello():
        return "Hello World !"
    
    register_blueprint(app)

    return app

app = create_app()