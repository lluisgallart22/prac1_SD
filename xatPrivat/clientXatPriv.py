import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc
import time

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = xatPrivat_pb2_grpc.GreeterStub(channel)
        texto = input("Por favor, introduce algo: ")
        response = stub.SendMessage(xatPrivat_pb2.MessageRequest(name=texto))
        print("Mensaje del servidor:", response.message)
        selecciona = input("A quin client et vols connectar?")
        response = stub.SendMessage(xatPrivat_pb2.MessageRequest(name=texto))


if __name__ == '__main__':
    run()