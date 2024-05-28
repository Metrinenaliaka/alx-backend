#!/usr/bin/env python3
"""
using babel.localeselector & request.accept_languages.best_match
"""

import gettext
from flask import Flask, request, render_template, g
from flask_babel import Babel, gettext
app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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
    locale = request.args.get('locale')
    if locale and locale in 'LANGUAGES':
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id: int) -> dict:
    """
    get user from mock database using id
    """
    return users.get(user_id)


@app.before_request
def before_request():
    login_as = request.args.get('login_as')
    if login_as:
        g.user = get_user(int(login_as))
    else:
        g.user = None


@app.route('/')
def home():
    if g.user:
        message = gettext("You are logged in as\
                          %(username)s.") % {'username': g.user['name']}
    else:
        message = gettext("You are not logged in.")
    return render_template('5-index.html', message=message)


if __name__ == "__main__":
    app.run()
