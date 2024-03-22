import pika
import json
from connect import create_connect
from models import Contact

create_connect()

def callback(ch, method, properties, body):
    """
    Callback function to process messages received from the queue.

    :param ch: The channel object.
    :param method: Method frame.
    :param properties: Properties frame.
    :param body: The message body, containing the contact ID.
    :return: None
    """
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects.with_id(contact_id)

    if contact:
        print(f" [x] Email sent to {contact.fullname} <{contact.email}>")
        contact.message_status = True
        contact.save()


def main():
    """
    Main function to start consuming messages from the 'send_by_email' queue,
    simulating the email sending process.
    """
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672,
                                  credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='send_by_email')

    channel.basic_consume(
        queue='send_by_email', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for email messages. To exit press CTRL+C.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping consuming...")
