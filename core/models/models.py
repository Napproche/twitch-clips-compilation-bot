from peewee import *
import datetime

import constants

db = SqliteDatabase(constants.DATABASE_LOCATION)


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    name = CharField()
    full = CharField()
    cli = CharField()


class Type(BaseModel):
    name = CharField()


class Destination(BaseModel):
    name = CharField()


class Channel(BaseModel):
    name = CharField()
    slug = CharField()
    logo = CharField()
    url = CharField()


class Video(BaseModel):
    title = CharField()
    date = DateTimeField(default=datetime.datetime.now)
    game = ForeignKeyField(Game)
    channel = ForeignKeyField(Channel, backref='videos', null=True)
    type = ForeignKeyField(Type)
    destination = ForeignKeyField(Destination, backref='videos')


class Clip(BaseModel):
    title = CharField()
    slug = CharField(unique=True)
    views = IntegerField()
    thumbnail = CharField()
    duration = DecimalField()
    date = DateTimeField()
    used_in_compilation_video = BooleanField()
    channel = ForeignKeyField(Channel, backref='clips')
    game = ForeignKeyField(Game, backref='clips')
    videos = ManyToManyField(Video, backref='clips')

VideoClips = Clip.videos.get_through_model()
