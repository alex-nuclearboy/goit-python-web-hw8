from mongoengine import Document 
from mongoengine.fields import (
    StringField,
    DateField,
    DateTimeField,
    BooleanField
)


class Contact(Document):
    fullname = StringField(required=True)
    birthday = DateField()
    address = StringField()
    email = StringField(required=True)
    phone = StringField(required=True)
    message_status = BooleanField(default=False)
    message_time = DateTimeField()
