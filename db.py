import random

from datetime import datetime, timedelta
from peewee import Model, CharField, ForeignKeyField, BooleanField, DateTimeField

from base.email import send_email
from publickeykeeper import database
"""
Secrets:
    Free:
        Will try not to have to keep any secrets for free accounts
    Paid:
        Keep only information required for payment
"""

public_id_types = ('Twitter', 'email')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    about = CharField(null=True)


class PublicId(BaseModel):
    """
    Id's such as email address, twitter id, .....
    """
    TWITTER = 'twitter'
    EMAIL = 'email'

    idtype = CharField(null=False)
    account = CharField(null=False)
    userid = ForeignKeyField(User, related_name='user')
    verifyed = BooleanField(default=False)
    code = CharField()
    code_expired_date = DateTimeField()

    def accept_verify(self):
        self.verifyed = True
        self.save()

    def refresh_code(self):
        now = datetime.now()
        if self.code_expired_date is None or self.code_expired_date < now:
            self.code = random.randint(100000, 999999)
            self.code_expired_date = now + timedelta(minutes=5)
            self.save()

    def send_code(self):
        if self.idtype == PublicId.EMAIL:
            subject = 'New code for publickeykeeper'
            body = 'Use this link to verify your email account: https://publickeykeeper.org/api/verify?key={}'.format(self.code)
            send_email(subject, self.account, body)

    class Meta:
        # constraints = [Check('idtype in public_id_types')]
        indexes = ((('idtype', 'account'), True), )


class Key(BaseModel):
    publicid = ForeignKeyField(PublicId, related_name='key')
    # As in what crypto tech was used. Now only RSA
    keytype = CharField(null=False)
    # if it is not unique we what should we do?
    # TODO: Convert to DER or PEM
    publickey = CharField(unique=True, null=False)

    @staticmethod
    def get_key(account, service):
        return Key.select().join(PublicId).where(PublicId.account == account, PublicId.idtype == service).get()
