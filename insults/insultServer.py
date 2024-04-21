import pika
import threading
import signal
import time

#creem una llista per saber tots els clients que tenim en el xat grupal
clients = []
insu = []

get_lock = threading.Lock()

def aturat(sig, frame):
	import sys
	channel.close()
	connection.close()
	sys.exit(0)
	
def connexio():
	parameters = pika.ConnectionParameters('localhost')
	return pika.BlockingConnection(parameters)

def client_nou(ch, method, properties, body):
	clients.append(body.decode())

def reb_miss(ch, method, properties, body):
	insu.append(body.decode())
	print("Insult arrivat ->", body.decode())
		
def env_miss(ch, method, properties, body):
	print(insu[0])
	if insu:
		insult = insu.pop(0)
		channel.basic_publish(exchange='', routing_key='miss_clients', body=insult, properties=pika.BasicProperties(delivery_mode=2))
		print("insult guardat a la cua")
	
	
parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='insults', durable=True)

channel.queue_declare(queue='info_clients', durable=True)

channel.queue_declare(queue='miss_clients', durable=True)

signal.signal(signal.SIGINT, aturat)

def inici_new():
	while True:
		try:
			with get_lock:
				method_frame, header_frame, body = channel.basic_get(queue='info_clients', auto_ack=True)
			if method_frame:
				client_nou(None, method_frame, None, body)
		except pika.exceptions.StreamLostError:
			print("S'ha perdut la connexió amb RabbitMQ.")
			break

def inici_reb():
	while True:
		try:
			with get_lock:
				method_frame, header_frame, body = channel.basic_get(queue='insults', auto_ack=True)
			if method_frame:
				reb_miss(None, method_frame, None, body)
			else:
				time.sleep(1)
		except pika.exceptions.StreamLostError:
			print("S'ha perdut la connexió amb RabbitMQ.")
			break

def inici_env():
	global connection, channel
	while True:
		try:
			if insu:
				inserir = insu.pop(0)
				with get_lock:
					channel.basic_publish(exchange='', routing_key='miss_clients', body=inserir, properties=pika.BasicProperties(delivery_mode=2))
				print("Missatge enviat")
		except pika.exceptions.StreamLostError:
			connection = connexio()
			channel = connection.channel()


thread_r = threading.Thread(target=inici_reb)
thread_r.start()

thread_n = threading.Thread(target=inici_new)
thread_n.start()

thread_e = threading.Thread(target=inici_env)
thread_e.start()

print('Esperan insults ...')

thread_n.join()
thread_r.join()
thread_e.join()