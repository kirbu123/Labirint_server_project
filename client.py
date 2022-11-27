import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = '!DISCONNECT'

SERVER = '172.29.16.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def Send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b'' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)
    print(client.recv(3000))

while True:
    msg = str(input())
    Send(msg)
