import peewee
from settings import db


class BizQuizModel(peewee.Model):
    class Meta:
        database = db


class Topic(BizQuizModel):
    name = peewee.CharField(unique=True)


class Article(BizQuizModel):
    topic = peewee.ForeignKeyField(Topic, related_name="topics")
    subject = peewee.CharField()
    body = peewee.CharField()
