from .extensions import mongo
from flask_login import UserMixin
from mongoengine import ObjectIdField
from bson import ObjectId

class Entities(mongo.EmbeddedDocument):
    entity = mongo.StringField(required=True)
    score = mongo.IntField(required=True)
    word = mongo.StringField(required=True)
    start_index = mongo.IntField(required=True)
    end_index = mongo.IntField(required=True)

class Note(mongo.EmbeddedDocument):
    id = ObjectIdField(default=ObjectId)
    text = mongo.StringField(required=True)
    entities =  mongo.EmbeddedDocumentListField(Entities)

class User(mongo.Document , UserMixin):
    email = mongo.StringField(required=True)
    name = mongo.StringField(required=True)
    password = mongo.StringField(required=True)
    notes = mongo.EmbeddedDocumentListField(Note)


