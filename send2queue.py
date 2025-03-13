import pika
import json

def publish_article(article_data):
    """Send scraped article data to RabbitMQ queue."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # Declare queue (ensures it exists)
    channel.queue_declare(queue="news_queue", durable=True)

    # Convert article dictionary to JSON
    message = json.dumps(article_data)

    # Publish article to RabbitMQ queue
    channel.basic_publish(
        exchange="",
        routing_key="news_queue",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Makes message persistent
    )

    print(f"📤 Sent article: {article_data['title']}")
    connection.close()
