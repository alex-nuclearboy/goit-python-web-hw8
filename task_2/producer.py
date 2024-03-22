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
    Creates fake contacts and saves them to the database.

    :param n: The number of fake contacts to create. Default is 10.
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
            message_status=True,
            message_time=message_time
        )
        contact.save()
        send_to_queue(str(contact.id), prefered_method)


def send_to_queue(contact_id, prefered_method):
    """
    Sends the given contact ID to a queue based on the preferred contact method.

    :param contact_id: The ID of the contact to be sent to the queue.
    :param prefer_method: The preferred method of contacting the user
                          (email or sms).
    return: None
    """

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

    # Send the contact ID to the appropriate queue
    channel.basic_publish(
        exchange='', routing_key=routing_key,
        body=json.dumps({'contact_id': contact_id}))
    print(f" [x] Sent contact ID {contact_id} to {routing_key} queue")
    connection.close()


if __name__ == '__main__':
    create_connect()
    print("Producer script started. Publishing messages to RabbitMQ...")
    create_fake_contacts(10)
