from flask import Flask, redirect, request, render_template, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def index():
    pass
