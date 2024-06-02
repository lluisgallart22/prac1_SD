import sys
import pika
import threading
import redis
from queue import Queue


lock = threading.Lock()
cola = Queue()
temps = 0
nomXat = sys.argv[1]
consumidor_activo=True

#Opcio per enviar missatges dins del xat
def enviar_mensaje():
    global consumidor_activo
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=nomXat, exchange_type='fanout', durable=True)
    
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
#Opcio usada per rebre tots els missatges que s'han enviat al xat grupal
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
#Aquesta funcio el que fa es agafar tots els missatges que s'han enviat avans de connectarse 
#i mostrar-los ja que tots els missatges son persistents, aquesta funcio sol se executa duran 1 segon ja que sol poder
#agafar els missatges i mostrarlos per terminal
def recibir_mensajes_persistentes():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

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
    connection.sleep(1)
    connection.close()
#Quan creem un nou xat emmagatzemem el xat al REDIS
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
        global temps
        channel.exchange_declare(exchange='descobrir xat', exchange_type='fanout')
        channel.basic_publish(exchange='descobrir xat', routing_key='', body=nomXat)
        temps =12
        
        


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    while consumidor_activo:
        connection.process_data_events()
    
    connection.close()



#Creacio de tots els threads
thread_recibir = threading.Thread(target=recibir_mensaje)
thread_enviar = threading.Thread(target=enviar_mensaje)
thread_recivir_persistent =  threading.Thread(target=recibir_mensajes_persistentes)
thread_guardar_redis = threading.Thread(target=guardar_nombre_chat)
thread_descobriment = threading.Thread(target=descobriment_xat)
#Iniciem els threadds
thread_guardar_redis.start()
thread_recivir_persistent.start()
thread_recibir.start()
thread_enviar.start()
thread_descobriment.start()
#Esperem les execucions dels threads
thread_guardar_redis.join()
thread_recivir_persistent.join()
thread_enviar.join()
thread_recibir.join()
thread_descobriment.join()