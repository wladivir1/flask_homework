from functools import cache
from flask import Flask


@cache
def get_app():
    app = Flask(__name__)
    return app
