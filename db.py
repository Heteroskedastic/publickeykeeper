from peewee import *
import datetime
import pandas as pd

DB = SqliteDatabase('publickeykeeper.db')

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
        database = DB


class Public_Id(BaseModel):
    """
    Id's such as email address, twitter id, .....
    """
    idtype = CharField(null=False)
    userid = CharField(null=False)

    class Meta:
        constraints = [Check('idtype in public_id_types')]
        indexes = ( (('idtype', 'userid'), True), )


class User(BaseModel):
    publicid = ForeignKeyField(Public_Id, related_name='user')
    firstname = CharField(null=True)
    lastname = CharField(null=True)
    about = CharField(null=True)


class Key(BaseModel):
    publicid = ForeignKeyField(Public_Id, related_name='key')
    keytype = CharField(null=False) # As in what crypto tech was used
    publickey = CharField(unique=True, null=False) # if it is not unique we what should we do?




