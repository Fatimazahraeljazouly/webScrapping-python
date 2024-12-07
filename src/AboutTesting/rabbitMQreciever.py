#!/usr/bin/env python
import pika
import sys
import os

def main():
    # Connect to RabbitMQ with credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',  # Hostname
        5672,  # Port (optional, defaults to 5672)
        '/',  # Virtual host (default is '/')
        pika.PlainCredentials('root', 'root')  # Username and Password
    ))
    channel = connection.channel()

    # Declare the queue (make it durable if needed)
    channel.queue_declare(queue='test_queue', durable=True)

    # Callback function to handle messages
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        # Acknowledge the message (optional but recommended for reliable delivery)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Start consuming messages from the queue
    channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        # Start processing incoming messages
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == '__main__':
    main()
