import pika
import json
from models import Contact
from faker import Faker
from connect import create_connect

fake_data = Faker()

def create_fake_contacts(n=10):
    for _ in range(n):
        birthday = fake_data.date_of_birth(minimum_age=18, maximum_age=80)
        contact = Contact(
            fullname=fake_data.name(),
            birthday=birthday,
            email=fake_data.email(),
            phone=fake_data.phone_number(),
        )
        contact.save()
        send_to_queue(str(contact.id))


def send_to_queue(contact_id):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672,
                                  credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_publish(
        exchange='', routing_key='email_queue',
        body=json.dumps({'contact_id': contact_id}))
    print(f" [x] Sent contact ID {contact_id} to queue")
    connection.close()


if __name__ == '__main__':
    create_connect()
    create_fake_contacts(10)
