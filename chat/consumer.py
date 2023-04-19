import json
import pika
from nomic.gpt4all import GPT4All
import time
from infochat.producer import publish

bot = GPT4All(model='gpt4all-lora-quantized')
bot.open()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='prompts')

def callback(ch, method, properties, body):
    print("\nPrompt recieved")
    data = json.loads(body)
    print(data)
    
    result = bot.prompt(data['prompt'])

    publish('result', result, data['userID'])


channel.basic_consume(queue='prompts', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()