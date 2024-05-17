import asyncio
import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc

class Xat(xatPrivat_pb2_grpc.XatServicer):
    def __init__(self):
        self.clients = {}

    async def SendMessage(self, request, context):
        sender = request.sender
        receiver = request.receiver
        text = request.text

        if receiver not in self.clients:
            return xatPrivat_pb2.MessageResponse(sender='Servidor', text=f'Client {receiver} no trobat')

        receiver_context = self.clients[receiver]
        await receiver_context.write(xatPrivat_pb2.MessageResponse(sender=sender, text=text))
        return xatPrivat_pb2.MessageResponse(sender='Servidor', text='Missatge enviat')

async def serve():
    server = grpc.aio.server()
    xatPrivat_pb2_grpc.add_XatServicer_to_server(Xat(), server)
    listen_addr = "[::]:50051"
    print(f"Activant servidor en el port {listen_addr}")
    server.add_insecure_port(listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

async def send_message():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = xatPrivat_pb2_grpc.XatStub(channel)

        sender = input("Introdueix el teu nom d'usuari:")
        receiver = input("Introdueix el nom del usuari a qui li vols enviar:")

        while True:
            text = input("Introdueix el missatge (o exit per sortir):")
            if text.lower() == 'exit':
                break

            response = await stub.SendMessage(xatPrivat_pb2.MessageRequest(sender=sender, receiver=receiver, text=text))
            print(response.text)

async def main():
    s = asyncio.create_task(serve())
    c = asyncio.create_task(send_message())

    await asyncio.gather(s, c)

if __name__ == "__main__":
    asyncio.run(main())
