#!/usr/bin/env python3
"""
using babel.localeselector & request.accept_languages.best_match
"""

from flask import Flask, request, render_template
from flask_babel import Babel


app = Flask(__name__)


class Config:
    """
    Configuring Babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Apply the configuration to the app
app.config.from_object(Config)

# Instantiate the Babel object and store it in a module-level variable
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match with
    our supported languages
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    render a html file
    """
    return render_template('2-index.html')


if __name__ == "__main__":
    app.run()
