from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongodb_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')

uri = (
    f'mongodb+srv://{mongodb_user}:{mongodb_pass}'
    '@cluster0.xts1vbl.mongodb.net/?retryWrites=true&'
    'w=majority&appName=Cluster0'
)


def create_connect():
    """
    Creates a connection with the MongoDB.
    """
    connect(db=db_name, host=uri, ssl=True)
