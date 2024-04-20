import grpc
from concurrent import futures
import xatPrivat_pb2
import xatPrivat_pb2_grpc

class GreeterServicer(xatPrivat_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.connected_clients = {}  # Diccionario para almacenar clientes conectados y sus contextos de comunicación

    def SendMessage(self, request, context):
        if request.name == "Connect":
            client_id = request.client_id
            client_ip = context.peer()  # Obtener la dirección IP del cliente
            self.connected_clients[client_id] = (client_ip, context)
            
            # Construir la lista de clientes conectados (identificación del cliente y dirección IP)
            connected_clients_list = [f"{client_id}: {client_info[0]}" for client_id, client_info in self.connected_clients.items()]
            connected_clients_string = "\n".join(connected_clients_list)
            
            return xatPrivat_pb2.MessageReply(message=f"Bienvenido, {client_id}!\nClientes conectados:\n{connected_clients_string}")

        elif request.name == "Send":
            client_id = request.client_id
            message = request.name
            if client_id in self.connected_clients:
                client_ip, context = self.connected_clients[client_id]
                # Envía el mensaje al cliente específico utilizando su contexto de comunicación
                context.send_initial_metadata((('client-id', client_id.encode()),))
                context.write(xatPrivat_pb2.MessageReply(message=message))
                context.done()
                return xatPrivat_pb2.MessageReply(message="Mensaje enviado con éxito.")
            else:
                return xatPrivat_pb2.MessageReply(message=f"Cliente {client_id} no encontrado.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
