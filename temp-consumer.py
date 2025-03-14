import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# Declare the same queue
channel.queue_declare(queue="news_queue", durable=True)

def callback(ch, method, properties, body):
    """Process and print messages in a structured format."""
    article = json.loads(body)

    print("\n===== New Article Received =====")
    print(f"Title: {article['title']}")
    print(f"Date: {article['pub_date']}")
    print(f"Link: {article['link']}")
    print(f"Image: {article['image']}")
    print(f"Source: {article['source']}")
    print("\nContent:\n" + article['content'])
    print("=" * 50)  # Separator line

    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

channel.basic_consume(queue="news_queue", on_message_callback=callback)

print("Waiting for messages. Press CTRL+C to exit.")
channel.start_consuming()
