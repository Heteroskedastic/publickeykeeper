import random

from datetime import datetime, timedelta
from sqlalchemy_utils.types.choice import ChoiceType
from werkzeug.security import generate_password_hash, check_password_hash

from base import db
"""
Secrets:
    Free:
        Will try not to have to keep any secrets for free accounts
    Paid:
        Keep only information required for payment
"""

public_id_types = ('Twitter', 'email')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=True)
    lastname = db.Column(db.String, nullable=True)
    about = db.Column(db.String, nullable=True)
    active = db.Column(db.Boolean, default=False)
    login = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    publicids = db.relationship('PublicId', backref=db.backref('publicid', lazy='joined', enable_typechecks=False), lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_anonymous():
        return False


class PublicId(db.Model):
    """
    Id's such as email address, twitter id, .....
    """
    TWITTER = 'twitter'
    EMAIL = 'email'
    IDS_TYPES = [
        (TWITTER, TWITTER),
        (EMAIL, EMAIL)
    ]

    __tablename__ = 'publicid'
    id = db.Column(db.Integer, primary_key=True)
    idtype = db.Column(ChoiceType(IDS_TYPES), nullable=False, index=True)
    account = db.Column(db.String(255), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    verifyed = db.Column(db.Boolean, default=False)
    code = db.Column(db.String(64))
    code_expired_date = db.Column(db.DateTime)
    key = db.relationship('Key', backref=db.backref('key', lazy='joined', enable_typechecks=False), lazy='dynamic')
    __table_args__ = (db.UniqueConstraint('idtype', 'account', name='_service_account'),)

    def accept_verify(self):
        self.verifyed = True
        db.session.commit()

    def refresh_code(self):
        now = datetime.now()
        if self.code_expired_date is None or self.code_expired_date < now:
            self.code = random.randint(100000, 999999)
            self.code_expired_date = now + timedelta(minutes=5)
            db.session.commit()

    def send_code(self):
        from base.email import send_email
        if self.idtype == PublicId.EMAIL:
            subject = 'New code for publickeykeeper'
            body = 'Use this link to verify your email account: https://publickeykeeper.org/api/verify?key={}'.format(self.code)
            send_email(subject, self.account, body)


class Key(db.Model):
    __tablename__ = 'key'
    id = db.Column(db.Integer, primary_key=True)
    publicid_id = db.Column(db.Integer, db.ForeignKey(PublicId.id), nullable=False)
    # As in what crypto tech was used. Now only RSA
    keytype = db.Column(db.String(64), nullable=False)
    # if it is not unique we what should we do?
    # TODO: Convert to DER or PEM
    publickey = db.Column(db.UnicodeText, unique=True, nullable=False)
