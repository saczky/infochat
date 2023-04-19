from django.shortcuts import render
from django.http import JsonResponse
from nomic.gpt4all import GPT4All
from .producer import publish
import json
import pika

# Create your views here.
def home(request):
   return render(request, 'infochat/home.html')

def prompt(request):
   print('prompted')
   if request.POST.get('action') == 'prompt':
      response_data = {}

      prompt = request.POST.get('prompt')
      body = {'userID':'userID', 'prompt':prompt}
      publish('prompted', body, 'prompts')

      connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
      channel = connection.channel()
      channel.queue_declare(queue='userID')

      def callback(ch, method, properties, body):
         print('got the result')
         channel.stop_consuming()
         response_data['result'] = json.loads(body)
         print(body)

      channel.basic_consume(queue='userID', on_message_callback=callback, auto_ack=True)
      channel.start_consuming()

      print('resturning')
      return JsonResponse(response_data)