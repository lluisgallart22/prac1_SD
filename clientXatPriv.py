import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc
import time

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = xatPrivat_pb2_grpc.GreeterStub(channel)
        response = stub.SendMessage(xatPrivat_pb2.MessageRequest(name='algo'))
        print("Mensaje del servidor:", response.message)

if __name__ == '__main__':
    run()