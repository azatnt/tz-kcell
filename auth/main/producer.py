#!/usr/bin/env python
import json
import pika
import uuid


class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='rabbitmq'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True, queue='')
        self.callback_queue = result.method.queue
        self.channel.basic_consume(on_message_callback=self.on_response,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self, method, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='registration_queue',
                                   properties=pika.BasicProperties(
                                         method,
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         delivery_mode=1
                                         ),
                                   body=json.dumps(body))
        if self.response is None:
        # while :
            self.connection.process_data_events(time_limit=2)
        return self.response


def publish(method, body):
    rpc = RpcClient()
    print("Requesting")
    response = rpc.call(method, body)
    return response
