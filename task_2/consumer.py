import pika
import json
import sys
from models import Contact
from connect import create_connect

def stub_send_email(contact_id):
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()
        print(f"Email sent to {contact.fullname} <{contact.email}>")

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    stub_send_email(contact_id)

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, 
                                  credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_consume(
        queue='email_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    create_connect()
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
