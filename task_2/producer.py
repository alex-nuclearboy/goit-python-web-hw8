import pika
import json
from models import Contact
from connect import create_connect
from faker import Faker
from random import choice
from datetime import datetime

fake_data = Faker('en_GB')

def create_fake_contacts(n=10):
    """
    Creates and saves a specified number of fake contacts to the database,
    and sends their IDs to RabbitMQ queues.

    :param n: The number of fake contacts to create. Defaults to 10.
    :return: None
    """
    Contact.drop_collection()
    for _ in range(n):
        birthday = fake_data.date_of_birth(minimum_age=18, maximum_age=80)
        prefered_method = choice(["email", "sms"])
        message_time = datetime.now()

        contact = Contact(
            fullname=fake_data.name(),
            birthday=birthday,
            address=fake_data.address(),
            email=fake_data.email(),
            phone=fake_data.phone_number(),
            prefered_method=prefered_method,
            message_time=message_time
        )
        contact.save()

        send_to_queue(str(contact.id), prefered_method)


def send_to_queue(contact_id, prefered_method):
    """
    Sends a contact ID to the appropriate RabbitMQ queue
    based on the contact's preferred contact method.

    :param contact_id: The ID of the contact.
    :param preferred_method: The contact's preferred method of communication
                             ('email' or 'sms').
    :return: None
    """

    # Establish a connection to the RabbitMQ server
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672,
                                  credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='send_by_email')
    channel.queue_declare(queue='send_by_phone')

    # Determine the routing key based on the preferred method
    routing_key = (
        'send_by_email' if prefered_method == 'email' else 'send_by_sms'
    )

    # Publish the contact ID to the selected queue
    channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=json.dumps({'contact_id': contact_id}))

    print(f" [x] Sent contact ID {contact_id} to {routing_key} queue")

    connection.close()


if __name__ == '__main__':
    create_connect()
    print("Producer script started. Publishing messages to RabbitMQ...")
    create_fake_contacts(10)
