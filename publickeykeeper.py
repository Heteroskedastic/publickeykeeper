from flask import Flask

app = Flask(__name__)


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
    app.run()
