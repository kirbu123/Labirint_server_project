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

def Get(conn):
    msg = conn.recv(2048).decode(FORMAT)
    return msg.split()

def Set(conn, msg):
    conn.send(' '.encode(FORMAT))
    conn.send(msg.encode(FORMAT))
    conn.send(' '.encode(FORMAT))

def Other(conn):
    global GAME
    for i in GAME:
        if i != conn:
            return i
    return conn


def handle_client(conn, addr):
    global GAME
    GAME.append(conn)
    while True:
        print(len(GAME))
        msg = Get(conn)
        for iter in msg:
            #print(print(str(addr) + ": " + str(iter)))
            if iter[0] == 'P':
                if len(GAME) < 2:
                    Set(GAME[0], iter)
                else:
                    Set(Other(conn), iter)
            elif iter[0] == 'S':
                print('---------------------------------------------------------------------')
                for i in GAME:
                    Set(i, iter)
                    Set(i, 'P#-280#260#0.0')



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
