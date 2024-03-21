import pika
import json
import sys
from models import Contact
from connect import create_connect

def stub_send_email(contact_id):
    """
    Sends an email to a contact based on the provided contact_id.

    param contact_id: The unique identifier of the contact
                      to whom the email will be sent.
    return: None
    """
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.message_sent = True
        contact.save()
        print(f"Email sent to {contact.fullname} <{contact.email}>")

def callback(ch, method, properties, body):
    """
    Callback function that is called when a message is received.

    param ch: The channel object
    param method: The method object
    param properties: The properties object
    param body: The body of the message
    return: None
    """
    data = json.loads(body)
    contact_id = data['contact_id']
    stub_send_email(contact_id)

def main():
    """
    Main function to establish a connection, declare a queue,
    and start consuming messages.
    """
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
    try:
        create_connect()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
