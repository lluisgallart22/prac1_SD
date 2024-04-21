import pika
import uuid
import threading

id_client = str(uuid.uuid4())

espera = threading.Lock()

def connexio():
	parameters = pika.ConnectionParameters('localhost')
	return pika.BlockingConnection(parameters)


def rebre_insult(ch, method, properties, body):
	print("Insult -> ", body.decode())

def enviar_ins():
	global connection, channel
	while True:
		try:
			insult = input("Insulta: ")
			with espera:
				channel.basic_publish(exchange='', routing_key='insults', body=insult, properties=pika.BasicProperties(delivery_mode=2))
			print("Insult enviat")
		except pika.exceptions.StreamLostError:
			connection = connexio()
			channel = connection.channel()
			
		
def inici():
	global connection, channel
	while True:
		try:
			with espera:
				method_frame, header_frame, body = channel.basic_get(queue='miss_clients', auto_ack=True)
			if method_frame:
				rebre_insult(None, method_frame, None, body)
		except pika.exceptions.StreamLostError:
			print("s'ha perdut la connexio")
			connection = connexio()
			channel = connection.channel()
			channel.basic_publish(exchange='', routing_key='info_clients', body=id_client, properties=pika.BasicProperties(delivery_mode=2))
			#break

connection = connexio()
channel = connection.channel()

channel.basic_publish(exchange='', routing_key='info_clients', body=id_client, properties=pika.BasicProperties(delivery_mode=2))

thread_c = threading.Thread(target=inici)
thread_c.start()
		
enviar_ins()

thread_c.join()