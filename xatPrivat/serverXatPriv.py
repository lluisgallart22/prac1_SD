import grpc
from concurrent import futures
import xatPrivat_pb2
import xatPrivat_pb2_grpc

Usuaris = []
contador = 0


class GreeterServicer(xatPrivat_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.connected_clients = {}  # Diccionario para almacenar clientes conectados y sus contextos de comunicación

    def SendMessage(self, request, context):
        global contador
        Usuari = ""
        if request.name == "Connect" :
            client_id = request.client_id
            self.connected_clients[client_id] = context
            Usuari = ""
            for client_id, client_context in self.connected_clients.items():
                Usuari = Usuari + "\n" + client_context.peer()
                return xatPrivat_pb2.MessageReply(message=f"Usuaris Connectats -> {Usuari}")

        else: 
            return xatPrivat_pb2.MessageReply(message=f"Message -> {request.name}!")
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()