import sys
import pika
import threading
import redis
from queue import Queue


lock = threading.Lock()
# Cola para la comunicación entre hilos
cola = Queue()
temps = 0
nomXat = sys.argv[1]
consumidor_activo=True

def enviar_mensaje():
    global consumidor_activo
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=nomXat, exchange_type='fanout', durable=True)
    #channel.exchange_declare(exchange='descobrir xat', exchange_type='fanout')
    #channel.basic_publish(exchange='descobrir xat', routing_key='', body='Nuevo chat creado: ' + nomXat)
    
    print("Chat grupal")
    while True:
        entrada = input()
        if entrada.lower() == 'exit':
            print("Saliendo del bucle.")
            consumidor_activo=False
            break
        else:
            print("Enviado correctamente")
            message = entrada
            channel.basic_publish(
                exchange=nomXat,
                routing_key='',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Hacer que el mensaje sea persistente
                ))
    
    connection.close()

def recibir_mensaje():
    global consumidor_activo
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=nomXat, exchange_type='fanout', durable=True)
    result = channel.queue_declare(queue='', durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=nomXat, queue=queue_name)

    def callback(ch, method, properties, body):
        print("Mensaje de chat grupal:", body.decode())

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False)
    while consumidor_activo:
        connection.process_data_events()
    
    connection.close()

def recibir_mensajes_persistentes():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declarar el intercambio y la cola con durabilidad
    channel.exchange_declare(exchange=nomXat, exchange_type='fanout', durable=True)
    queue_name = 'persistent_queue_' + nomXat
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=nomXat, queue=queue_name)

    def callback(ch, method, properties, body):
        print(f"Mensaje de chat grupal: {body.decode()}")

    # Configurar el consumidor para usar la función de callback
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False)

    print('Esperando mensajes. Presiona Ctrl+C para salir.')
    # Esperar 2 segundos antes de detener el consumo
    connection.sleep(1)
    # Detener el consumo
    connection.close()

def guardar_nombre_chat():
    try:
        # Conexión a Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        # Guardar el nombre del chat en Redis
        r.set(nomXat, "Chat1Grupal")
    except Exception as e:
        print(f"Error al guardar el nombre del chat en Redis: {e}")

def descobriment_xat():
    global consumidor_activo
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
    while consumidor_activo:
        connection.process_data_events()
    
    connection.close()



# Crear e iniciar los hilos
thread_recibir = threading.Thread(target=recibir_mensaje)
thread_enviar = threading.Thread(target=enviar_mensaje)
thread_recivir_persistent =  threading.Thread(target=recibir_mensajes_persistentes)
thread_guardar_redis = threading.Thread(target=guardar_nombre_chat)

thread_descobriment = threading.Thread(target=descobriment_xat)

thread_guardar_redis.start()
thread_recivir_persistent.start()
thread_recibir.start()
thread_enviar.start()
thread_descobriment.start()

#Esperar a que ambos hilos terminen
thread_guardar_redis.join()
thread_recivir_persistent.join()
thread_enviar.join()
thread_recibir.join()
thread_descobriment.join()