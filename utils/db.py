import os
import datetime

from mongoengine import (
    connect,
    BooleanField,
    DateTimeField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField,
    URLField,
    IntField,
)
from mongoengine_mate import ExtendedDocument

from dotenv import load_dotenv
load_dotenv()

if os.environ.get("MONGODB_URI"):
    connect(host=os.environ.get("MONGODB_URI"))
else:
    raise Exception("No MongoDB URI specified.")


class Identity(EmbeddedDocument):
    name = StringField()
    phone = StringField()
    email = EmailField()
    address = StringField()


class Article(ExtendedDocument):
    # primary fields
    title = StringField()
    url = URLField(unique=True)
    timestamp = DateTimeField()

    # additional fields
    recruiting_status = StringField()
    sex = ListField(StringField(), default=['male', 'female'])
    target_disease = StringField()
    intervention = StringField()
    sponsor = StringField()
    summary = StringField()
    location = StringField()
    institution = StringField()
    contact = EmbeddedDocumentField(Identity)

    # optional fields
    sample_size = IntField()
    abandoned = BooleanField()
    abandoned_reason = StringField()

    # default sort timestamp descending
    meta = {
        "ordering": ["-timestamp"],
    }

    def __str__(self):
        return self.url


def create(articles):
    """
    Input: list of articles (dictionaries).
    Output: None

    Posts a list of articles to Mongo.
    """
    objects = []
    for a in articles:
        obj = Article(**a)
        objects.append(obj)
    Article.smart_insert(objects)
