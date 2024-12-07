import pika
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def callback(ch, method, properties, body):
    try:
        # Parse the JSON data
        data = json.loads(body)
        logging.info(f"Received message from {method.routing_key}: {data}")

        # Add your processing logic here

        # Manually acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        # Optionally, do not acknowledge to requeue the message
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def consume_from_rabbitmq():
    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost',  # Hostname
            5672,  # Port
            '/',  # Virtual host
            pika.PlainCredentials('root', 'root')  # Username and password
        ))
        channel = connection.channel()

        # Declare the exchange
        channel.exchange_declare(exchange='scraped_data_exchange', exchange_type='direct', durable=True)

        # Declare and bind queues
        queues = {
            'jumia_queue': 'jumia',
            'marjane_queue': 'marjane',
            'electroplanet_queue': 'electroplanet'
        }
        for queue, routing_key in queues.items():
            channel.queue_declare(queue=queue, durable=True)
            channel.queue_bind(exchange='scraped_data_exchange', queue=queue, routing_key=routing_key)

        # Start consuming messages
        for queue in queues.keys():
            channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)

        logging.info("Waiting for messages...")
        channel.start_consuming()

    except KeyboardInterrupt:
        logging.info("Interrupted by user. Closing connection...")
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"RabbitMQ connection error: {e}")
    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection.is_open:
            connection.close()
            logging.info("Connection closed.")


# Start the consumer
if __name__ == "__main__":
    consume_from_rabbitmq()
