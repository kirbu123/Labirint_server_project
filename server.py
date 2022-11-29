import random
import socket
import threading

HEADER = 64
PORT = 5050
LEN_GRIG = 659
SERVER = '192.168.43.239' #socket.gethostbyname(socket.gethostname()) #'172.29.16.1'


ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = '!DISCONNECT'
SETGRID_MESSAGE = '!SETGRID'
GAME = []
PRIORITY = {}

def Get(conn):
    msg = conn.recv(2048).decode(FORMAT)
    return msg.split()

def Set(conn, msg):
    conn.send(' '.encode(FORMAT))
    conn.send(msg.encode(FORMAT))
    conn.send(' '.encode(FORMAT))

def handle_client(conn, addr):
    global GAME, PRIORITY
    if len(GAME) == 1:
        other = GAME[0]
    else:
        other = conn
    PRIORITY[conn] = 0
    GAME.append(conn)
    count = 0
    for i in PRIORITY:
        if count == 0:
            PRIORITY[i] = 1
        else:
            PRIORITY[i] = 0
        count += 1
    while True:
        if len(GAME) == 1:
            other = conn
        msg = Get(conn)
        for iter in msg:
            print(print(str(addr) + ": " + str(iter)))
            if iter[0] == 'P':
                Set(other, iter)
            elif iter[0] == 'S':
                print('---------------------------------------------------------------------')
                if PRIORITY[conn] == 1:
                    Set(other, iter)
                    Set(other, 'P#-280#260#0.0')



def start():
    server.listen()
    print('LISTENNING on ' + str(SERVER))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print('ACTIVE CONNECTIONS: ' + str(threading.active_count() - 1))

print("STARTING server starting...")
start()
#END
