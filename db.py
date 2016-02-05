from peewee import Model, CharField, ForeignKeyField, Check

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
    idtype = CharField(null=False)
    account = CharField(null=False)
    userid = ForeignKeyField(User, related_name='user')

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
