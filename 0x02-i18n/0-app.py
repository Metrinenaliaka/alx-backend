#!/usr/bin/env python3
"""
a simple flask app
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    render a html file
    """
    return render_template('0-index.html')
