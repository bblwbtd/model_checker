from peewee import *

db = SqliteDatabase("db.sqlite")


class BaseModel(Model):
    class Meta:
        database = db


class Template(BaseModel):
    name = TextField(null=False)
    content = TextField(null=False)


db.create_tables(BaseModel.__subclasses__())
