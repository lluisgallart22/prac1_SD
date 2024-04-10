import grpc
from concurrent import futures
import xatPrivat_pb2
import xatPrivat_pb2_grpc

class GreeterServicer(xatPrivat_pb2_grpc.GreeterServicer):
    def SendMessage(self, request, context):
        return xatPrivat_pb2.HelloReply(message=f"Message -> {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()