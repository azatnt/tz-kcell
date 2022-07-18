import json
import pika

from django.contrib.auth.models import User
from main.service import check_and_create_contact, get_contact_by_user, get_all_users_and_contacts, \
    get_all_contacts_grouped_by_user

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='registration_queue', durable=True)


def on_request(ch, method, props, body):
    contacts = json.loads(body)
    result = None
    if props.content_type == 'contact_create':
        user = User.objects.get(username = contacts['username'])
        del contacts['username']
        if check_and_create_contact(user, contacts):
            result = "Contact created"
        else:
            result = "Contact with that credentials already exists!"
    elif props.content_type == 'contact_get_by_user':
        user_id = contacts['id']
        user_with_contacts = get_contact_by_user(user_id)
        if user_with_contacts is None:
            result = f"User with id={user_id} doesn't exist!"
        else:
            result = user_with_contacts
    elif props.content_type == 'contact_get_all':
        result = get_all_contacts_grouped_by_user()
    else:
        result = get_all_users_and_contacts()

    properties = pika.BasicProperties(correlation_id=props.correlation_id)
    channel.basic_publish(exchange='', routing_key=props.reply_to, properties=properties, body=json.dumps(result))


def consumer():
    channel.basic_consume(on_message_callback=on_request, queue='registration_queue', auto_ack=True)
    print("Awaiting RPC requests")
    channel.start_consuming()
