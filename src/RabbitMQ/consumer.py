import pika
import json
from src.MarjanScrapper.marjanTEST import scrape_marjane
from src.JumiaScrapper.jumia import scrape_jumia
from src.ElectroScrapper.electroPlanet import scrape_electroplanet

def send_scraped_data_to_rabbitmq(data, website):
    """
    Sends the scraped JSON data directly to RabbitMQ.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost',  # Hostname
            5672,  # Port
            '/',  # Virtual host
            pika.PlainCredentials('root', 'root')  # Username and password
        ))
    channel = connection.channel()

    # Declare the exchange for scraped data
    channel.exchange_declare(exchange='scraped_data_exchange', exchange_type='direct', durable=True)

    # Publish the data to RabbitMQ
    channel.basic_publish(
        exchange='scraped_data_exchange',
        routing_key=website,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )

    print(f"Data for {website} sent to RabbitMQ.")
    connection.close()


def callback(ch, method, properties, body):
    """
    Handles the request to scrape data for a specific website.
    """
    website = body.decode('utf-8')
    print(f"Received scraping request for: {website}")

    # Define scraper mapping
    scrapers = {
        'jumia': scrape_jumia,
        'marjane': scrape_marjane,
        'electroplanet': scrape_electroplanet
    }

    if website in scrapers:
        try:
            # Execute the scraper and get the data
            data = scrapers[website]()  # The scraper function should return a dictionary or list
            print(f"Successfully scraped data for {website}.")

            # Send the data to RabbitMQ
            send_scraped_data_to_rabbitmq(data, website)

        except Exception as e:
            print(f"Error scraping {website}: {e}")
    else:
        print(f"No scraper found for {website}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """
    Main function to consume messages from RabbitMQ.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost',  # Hostname
            5672,  # Port
            '/',  # Virtual host
            pika.PlainCredentials('root', 'root')  # Username and password
        ))

    channel = connection.channel()

    # Declare the queue for scraper requests
    channel.queue_declare(queue='scraper_requests', durable=True)

    # Consume messages
    channel.basic_consume(queue='scraper_requests', on_message_callback=callback)

    print("Waiting for scraping requests...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
