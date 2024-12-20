import pika

def send_scraping_request(website):
    """
    Sends a test scraping request to the RabbitMQ queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',  # Hostname
        5672,         # Port
        '/',          # Virtual host
        pika.PlainCredentials('root', 'root')  # Username and password
    ))
    channel = connection.channel()

    # Declare the queue (must match the consumer's queue)
    channel.queue_declare(queue='scraper_requests', durable=True)

    # Publish a message to the queue
    channel.basic_publish(
        exchange='',  # Default exchange
        routing_key='scraper_requests',
        body=website,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )

    print(f"Sent scraping request for: {website}")
    connection.close()


if __name__ == "__main__":
    # Test with different websites
    websites = ['jumia', 'marjane', 'electroplanet']

    for site in websites:
        send_scraping_request(site)
