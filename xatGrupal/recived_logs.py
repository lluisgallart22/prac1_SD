import sys
import pika
import threading
from queue import Queue


lock = threading.Lock()
# Cola para la comunicación entre hilos
cola = Queue()
temps = 0
nomXat = sys.argv[1]

def enviar_mensaje():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=nomXat, exchange_type='fanout')
    #channel.exchange_declare(exchange='descobrir xat', exchange_type='fanout')
    #channel.basic_publish(exchange='descobrir xat', routing_key='', body='Nuevo chat creado: ' + nomXat)
    
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
        print("Mensaje de chat grupal:", body.decode())

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
    connection.close()

def descobriment_xat():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='descobrir xat', queue=queue_name)
    


    def callback(ch, method, properties, body):
        #method_frame, header_frame, body = channel.basic_get(queue=queue_name)
        global temps
        # Aquí es donde se publicaría el mensaje para notificar al código de descubrimiento
        channel.exchange_declare(exchange='descobrir xat', exchange_type='fanout')
        channel.basic_publish(exchange='descobrir xat', routing_key='', body=nomXat)
        #channel.basic_cancel(consumer_tag=method_frame.consumer_tag)
        temps =12
        


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
    connection.close()
    



# Crear e iniciar los hilos
thread_enviar = threading.Thread(target=enviar_mensaje)
thread_recibir = threading.Thread(target=recibir_mensaje)
thread_descobriment = threading.Thread(target=descobriment_xat)


thread_enviar.start()
thread_recibir.start()
thread_descobriment.start()

# Esperar a que ambos hilos terminen
thread_enviar.join()
thread_recibir.join()
thread_descobriment.join()
