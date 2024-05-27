import sys
import pika
import threading
from queue import Queue
import redis

redis_host = 'localhost'
redis_port = 6379
redis_db = 1
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

lock = threading.Lock()
cola = Queue()
temps = 0
nomXat = sys.argv[1]
consumidor_activo = True

def enviar_mensaje():
    global consumidor_activo
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials('a', '1234')  # Cambiar por tus credenciales
        )
    )

    channel = connection.channel()
    
    if not r.exists(f'nom:{nomXat}'):
        # Si la cola no existe, la declaramos
        channel.exchange_declare(exchange=nomXat, exchange_type='fanout', durable=True)
        result = channel.queue_declare(queue='', exclusive=True, durable=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=nomXat, queue=queue_name)
        r.hset(f'nom:{nomXat}', mapping={
            'ip': 'localhost',
            'port': 0,
            'db': 1
        })
    
    print("Chat grupal")
    while True:
        entrada = input()
        if entrada.lower() == 'exit':
            print("Saliendo del bucle.")
            consumidor_activo = False
            break
        else:
            print("Enviado correctamente")
            message = entrada
            channel.basic_publish(exchange=nomXat, routing_key='', body=message, properties=pika.BasicProperties(delivery_mode=2,))
    
    connection.close()


def consumir_mensajes_anteriores(channel, queue_name):
    for method_frame, properties, body in channel.consume(queue_name, inactivity_timeout=1):
        if method_frame is None:
            break
        print("Mensaje de chat grupal:", body.decode())
        channel.basic_ack(method_frame.delivery_tag)


def recibir_mensaje():
    global consumidor_activo
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=pika.PlainCredentials('a', '1234')  # Cambiar por tus credenciales
        )
    )

    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True, durable=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=nomXat, queue=queue_name)

    # Iniciar el hilo para consumir mensajes anteriores
    consume_thread = threading.Thread(target=consumir_mensajes_anteriores, args=(channel, queue_name))
    consume_thread.start()
    
    # Esperar a nuevos mensajes
    print("Esperando nuevos mensajes...")
    while consumidor_activo:
        connection.process_data_events()
    
    connection.close()

# Crear e iniciar los hilos
thread_enviar = threading.Thread(target=enviar_mensaje)
thread_recibir = threading.Thread(target=recibir_mensaje)

thread_enviar.start()
thread_recibir.start()

# Esperar a que ambos hilos terminen
thread_enviar.join()
thread_recibir.join()
