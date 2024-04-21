import asyncio
import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc

class Xat(xatPrivat_pb2_grpc.XatServicer):
    def SendMessage(self, request, context):
        sender = request.sender
        text = request.sender
        print(f"Missatge de {request.sender}: {request.text}")

        text = input("Que vols dir: ")
        response = xatPrivat_pb2.MessageResponse(sender='Servidor', text=text)
        yield response

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

if __name__ == "__main__":
    asyncio.run(serve())
