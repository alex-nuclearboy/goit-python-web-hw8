import json
from datetime import datetime
from models import Authors, Quotes
from connect import create_connect


def load_authors():
    Authors.drop_collection()
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors = json.load(f)
        for a in authors:
            author = Authors(
                fullname=a['fullname'],
                born_date=datetime.strptime(a['born_date'], '%B %d, %Y'),
                born_location=a['born_location'],
                description=a['description']
            )
            author.save()


def load_quotes():
    Quotes.drop_collection()
    with open('qoutes.json') as f:
        quotes = json.load(f)
        for q in quotes:
            for a in Authors.objects:
                if a.fullname == q['author']:
                    author = a
                    break
            quote = Quotes(
                tags=q['tags'],
                author=author,
                quote=q['quote']
            )
            quote.save()


if __name__ == '__main__':
    create_connect()
    load_authors()
    load_quotes()
