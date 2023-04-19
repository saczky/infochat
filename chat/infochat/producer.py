import json
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

def publish(method, body, queue):
    print('publishing...')
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
    print(f'published: {body}')
