import pika
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_to_rabbitmq(file_path, routing_key):
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

        # Read the JSON file
        with open(file_path, 'r') as file:
            data = file.read()

        # Publish the message
        channel.basic_publish(
            exchange='scraped_data_exchange',
            routing_key=routing_key,
            body=data,
            properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
        )
        logging.info(f"Sent {file_path} to RabbitMQ with routing key '{routing_key}'")

    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found.")
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"RabbitMQ connection error: {e}")
    finally:
        # Ensure the connection is closed
        if 'connection' in locals() and connection.is_open:
            connection.close()
            logging.info("Connection closed.")


# Send JSON files
if __name__ == "__main__":
    send_to_rabbitmq('../JumiaScrapper/jumia.json', 'jumia')
    send_to_rabbitmq('../MarjanScrapper/marjane_data.json', 'marjane')
    send_to_rabbitmq('../ElectroScrapper/electroplanet.json', 'electroplanet')
