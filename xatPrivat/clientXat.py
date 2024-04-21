import asyncio
import grpc
import xatPrivat_pb2
import xatPrivat_pb2_grpc

async def send_messages():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = xatPrivat_pb2_grpc.XatStub(channel)

        while True:
            text = input("Que vols dir: ")
            if text.lower() == 'exit':
                break
            async for response in stub.SendMessage(xatPrivat_pb2.MessageRequest(sender='Client', text=text)):
                print(f"Missatge rebut de {response.sender}: {response.text}")

async def main():
    await send_messages()

if __name__ == "__main__":
    asyncio.run(main())
