import peewee

from flask import Flask, g
from flask.ext.mail import Mail

from celery_app import make_celery
from config import TEMPLATE_DIR, STATIC_DIR, DATABASE

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config.from_object('config')
database = peewee.SqliteDatabase(DATABASE)

# register urls
from urls import *
register_api_urls(app)
register_base_urls(app)

celery = make_celery(app)
mail = Mail(app)


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'Hello World! from the index'


@app.route('/lookup')
def lookup():
    """
    Lookup user public key.
    Given:
       idtype (twitter, email, ...)
       userid (twitter id, email address.....)
    return: tuple, (keytype, publickey)
    """
    # TODO: Add lookup logic
    return 'Lookup key by "idtype, userid" '


if __name__ == '__main__':
    from db import User, PublicId, Key
    for model in [User, PublicId, Key]:
        try:
            model.create_table()
        except:
            pass
    app.run()
