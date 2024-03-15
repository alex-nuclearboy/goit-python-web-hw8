from mongoengine import Document 
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
