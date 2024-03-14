import json
from models import Authors, Quotes
from connect import create_connect

with open('authors.json', 'r', encoding='utf-8') as f:
    authors = json.load(f)
    for a in authors:
        author = Authors(
            fullname=a['fullname'],
            born_date=a['born_date'],
            born_location=a['born_location'],
            description=a['description']
        )
        author.save()

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
