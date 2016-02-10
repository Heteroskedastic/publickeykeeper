from flask import Flask
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy

from celery_app import make_celery
from config import TEMPLATE_DIR, STATIC_DIR

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config.from_object('config')
db = SQLAlchemy(app)

celery = make_celery(app)
mail = Mail(app)


# register urls
from urls import *
register_api_urls(app)
register_base_urls(app)


@app.route('/')
def index():
    return 'Hello World! from the index'
