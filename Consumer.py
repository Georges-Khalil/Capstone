import pika

# Callback function to handle the received message
def callback(ch, method, properties, body):
    print(f"Received: {body.decode()}")

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# Declare the queue (should be the same name as the producer's queue)
channel.queue_declare(queue="news_queue", durable=True)

# Set up the consumer to listen for messages from the queue
channel.basic_consume(queue="news_queue", on_message_callback=callback, auto_ack=True)

# Print a message indicating the consumer is waiting for messages
print("Waiting for messages. To exit, press CTRL+C")

# Start consuming messages from the queue
channel.start_consuming()

# testing