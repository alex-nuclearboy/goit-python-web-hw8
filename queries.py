import sys
import redis
from redis_lru import RedisLRU
from models import Authors, Quotes
from connect import create_connect
from mongoengine.errors import DoesNotExist

# Initialize connection to Redis for caching results
client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_quotes_by_name(query_value):
    """
    Searches for quotes by the author name.

    :param query_value: The author's name to search for.
    :return: A list of quotes by the specified author.
    """
    result = []
    try:
        author = Authors.objects.get(fullname__istartswith=query_value)
    except DoesNotExist:
        print(f"No author found starting with {query_value}.")
        return result

    quotes = Quotes.objects(author=author)
    if quotes:
        print(f"Quotes by {author.fullname}:")
        for quote in quotes:
            result.append(quote.quote)
    else:
        print("There are no quotes by this author.")
    return result


@cache
def search_quotes_by_tag_prefix(query_value):
    """
    Searches for quotes that contain tags starting with the specified prefix.

    :param query_value: The tag prefix to search for.
    :return: A list of quotes that have a matching tag.
    """
    result = []
    matching_quotes = Quotes.objects(tags__iregex=f'^{query_value}')

    tag_list = set()
    for quote in matching_quotes:
        for tag in quote.tags:
            if tag.startswith(query_value):
                tag_list.add(tag)

    if matching_quotes:
        print(f'Quotes with tags "{", ".join(tag_list)}":')
        for quote in matching_quotes:
            matching_tags = "; ".join(
                [tag for tag in quote.tags if tag in tag_list]
            )
            result.append(
                f'{quote.author.fullname} '
                f'[{matching_tags}]: '
                f'{quote.quote}'
            )
    else:
        print(f'There are no quotes with tags starting with "{query_value}".')
    return result


@cache
def search_quotes_by_tags(query_value):
    """
    Searches for quotes that have any of the specified tags.

    :param query_value: A comma-separated string of tags to search for.
    :return: A list of quotes that have any of the specified tags.
    """
    result = []
    tag_list = [tag.strip() for tag in query_value.split(",")]
    matching_quotes = Quotes.objects(tags__in=tag_list)

    if matching_quotes:
        print(f'Quotes with the tags "{query_value}":')
        for quote in matching_quotes:
            matching_tags = "; ".join(
                [tag for tag in quote.tags if tag in tag_list]
            )
            result.append(
                f'{quote.author.fullname} '
                f'[{matching_tags}]: '
                f'{quote.quote}'
            )
    else:
        print(f'No quotes found with tags "{query_value}"')

    return result


def main():
    """
    Main function to handle user input and execute search commands.
    """
    create_connect()
    while True:
        query = input("Enter the command: ").split(":")
        match query[0]:
            case "exit":
                sys.exit()
            case "name":
                quotes = search_quotes_by_name(query[1].strip())
                [print(quote) for quote in quotes]
                print()
            case "tag":
                quotes = search_quotes_by_tag_prefix(query[1].strip())
                [print(quote) for quote in quotes]
                print()
            case "tags":
                quotes = search_quotes_by_tags(query[1].strip())
                [print(quote) for quote in quotes]
                print()
            case _:
                print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
