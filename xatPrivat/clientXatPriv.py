import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc
import threading

def listen_for_messages(stub):
    while True:
        response = stub.SendMessage(xatPrivat_pb2.Empty())
        print("Mensaje del servidor:", response.message)
        # Puedes agregar aquí la lógica para manejar el mensaje recibido
        
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = xatPrivat_pb2_grpc.GreeterStub(channel)
        
        # Envía un mensaje 'Connect' al servidor al iniciar la conexión
        id = input("Id usuari: ")
        connect_response = stub.SendMessage(xatPrivat_pb2.MessageRequest(name="Connect", client_id=id))
        print("Mensaje del servidor:", connect_response.message)
        
        # Inicia un hilo para escuchar mensajes del servidor
        #message_listener = threading.Thread(target=listen_for_messages, args=(stub,))
        #message_listener.start()
        
        # Envía mensajes al servidor
        while True:
            texto = input("Por favor, introduce algo: ")
            id = input("Id del usuario: ")
            response = stub.SendMessage(xatPrivat_pb2.MessageRequest(name=texto, client_id=id))


if __name__ == '__main__':
    run()
