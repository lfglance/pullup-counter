from datetime import datetime

from peewee import *

from app import config


db = SqliteDatabase(f"{config.DATA_PATH}/sqlite.db")


class Pullup(Model):
    date = DateTimeField(default=datetime.utcnow)    
    clean = IntegerField(null=True)
    negative = IntegerField(null=True)
    pushup = IntegerField(null=True)

    class Meta:
        database = db


db.create_tables([Pullup])