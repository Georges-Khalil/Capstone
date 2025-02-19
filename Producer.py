import pika

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# Declare a queue named "news_queue" with durability set to True
channel.queue_declare(queue="news_queue", durable=True)

# Message to be sent
message = "Hello, this is a test news article!"

# Publish the message to the queue with properties to make it persistent
channel.basic_publish(
    exchange="",
    routing_key="news_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=2)  # Makes the message persistent
)

# Print confirmation message
print(f"Sent: {message}")

# Close the connection to RabbitMQ
connection.close()
