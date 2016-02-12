from flask.ext.mongoengine import Document
from mongoengine import StringField, URLField, ObjectIdField, DateTimeField

class Khabar(Document):
  _id         = ObjectIdField()
  title       = StringField()
  link        = URLField()
  description = StringField()
  img         = URLField()
  date        = DateTimeField()
  pubdate     = DateTimeField()
  source      = URLField()
  country     = StringField()
  domain      = URLField()
  category    = StringField()
  lang        = StringField()
  meta        = { 'collection': 'production',
                  'allow_inheritance': False
                }
