import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())
import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc
from concurrent import futures
import argparse
import threading
import redis

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0)

def get_port_from_redis(user):
    r = get_redis_connection()
    key = f'nom:{user}'
    port = r.hget(key, 'port')
    if port is None:
        raise ValueError(f"Port not found for user {user}")
    return int(port)

class Xat(xatPrivat_pb2_grpc.XatServicer):
    def SendMessage(self, request, context):
        print(f"Mensaje recibido de {request.sender}: {request.text}")
        response = xatPrivat_pb2.MessageResponse(sender=request.sender, text=request.text)
        print(f"Enviando mensaje a {request.receiver}: {request.text}")
        return response

def serve(port, sender):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_XatServicer_to_server(Xat(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor escuchando en el puerto {port}")

    def send_messages():
        while True:
            receiver = input("Ingrese el nombre de usuario del destinatario: ")
            try:
                receiver_port = get_port_from_redis(receiver)
                text = input("Ingrese el mensaje: ")
                send_message(receiver_port, sender, receiver, text)
            except ValueError as e:
                print(e)

    send_thread = threading.Thread(target=send_messages)
    send_thread.daemon = True
    send_thread.start()

    server.wait_for_termination()

def send_message(port, sender, receiver, text):
    channel = grpc.insecure_channel(f'localhost:{port}')
    stub = xatPrivat_pb2_grpc.XatStub(channel)
    request = xatPrivat_pb2.MessageRequest(sender=sender, receiver=receiver, text=text)
    response_future = stub.SendMessage(request, wait_for_ready=True)
    response_future.add_done_callback(lambda response_future: print(f"Mensaje enviado a {receiver}: {text}"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor gRPC para Xat')
    parser.add_argument('--port', type=int, default=50051, help='Puerto en el que escuchar')
    parser.add_argument('--sender', type=str, required=True, help='Nombre del usuario que envía los mensajes')
    args = parser.parse_args()
    serve(args.port, args.sender)