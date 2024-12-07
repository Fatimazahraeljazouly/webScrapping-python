import pika

# Connexion à RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost',  # Hostname
    5672,         # Port (optional, defaults to 5672)
    '/',          # Virtual host (default is '/')
    pika.PlainCredentials('root', 'root')  # Username and Password
))
channel = connection.channel()

# Déclaration de la queue (with durable flag)
channel.queue_declare(queue='test_queue', durable=True)

# Envoi d'un message
message = "Hello from RabbitMQ!"
channel.basic_publish(
    exchange='',
    routing_key='test_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # Make the message persistent
    )
)
print(f"Message envoyé : {message}")

# Fermeture de la connexion
connection.close()
