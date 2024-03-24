import sys
import pika
import threading
from queue import Queue

# Cola para la comunicación entre hilos
cola = Queue()

nomXat = sys.argv[1]

def enviar_mensaje():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=nomXat, exchange_type='fanout')

    print("Chat grupal")
    while True:
        entrada = input()
        if entrada.lower() == 'exit':
            print("Saliendo del bucle.")
            break
        else:
            print("Enviado correctamente")
            message = entrada
            channel.basic_publish(exchange=nomXat, routing_key='', body=message)
    
    connection.close()

def recibir_mensaje():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=nomXat, queue=queue_name)

    def callback(ch, method, properties, body):
        print(f"[x] {body}")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
    connection.close()

# Crear e iniciar los hilos
thread_enviar = threading.Thread(target=enviar_mensaje)
thread_recibir = threading.Thread(target=recibir_mensaje)

thread_enviar.start()
thread_recibir.start()

# Esperar a que ambos hilos terminen
thread_enviar.join()
thread_recibir.join()
