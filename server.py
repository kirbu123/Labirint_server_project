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

def handle_client(conn, addr):
    global GAME
    GAME.append(conn)
    print('NEW_CONNECTION: ' + str(addr) + " connected: ")
    connected = True
    while connected:

        other = conn
        for i in range(len(GAME)):
            if GAME[i] != conn:
                other = GAME[i]
                break

        msg = Get(conn)
        print(str(addr) + ' SENT: ' + str(msg))
        for i in range(len(msg)):
            Set(other, msg[i])


    print("[BREAK] connection")
    for i in range(len(GAME)):
        if GAME[i][0] == conn:
            GAME.pop(i)
            break
    conn.close()

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
