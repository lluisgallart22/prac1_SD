import pika

# Establecer la conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Obtener una lista de todas las colas
queue_names = channel.queues()

# Imprimir el nombre de cada cola
print("Colas en RabbitMQ:")
for queue in queue_names:
    print(queue.name)

# Cerrar la conexión
connection.close()
