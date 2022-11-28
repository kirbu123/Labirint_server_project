import socket
import threading

HEADER = 64
PORT = 5050
SERVER = '192.168.31.151' #socket.gethostbyname(socket.gethostname()) #'172.29.16.1'


ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = '!DISCONNECT'
GAME = []

def handle_client(conn, addr):
    global GAME
    GAME.append([conn, ''])
    print('NEW_CONNECTION: ' + str(addr) + " connected: ")
    connected = True
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)
            for i in range(len(GAME)):
                if GAME[i][0] == conn:
                    GAME[i][1] = msg
            if msg == DISCONNECTED_MESSAGE:
                connected = False
            print(str(addr) + ' SENT: ' + str(msg))
            count = 0
            for c in GAME:
                for i in GAME:
                    if i != c:
                        count += 1
                        c[0].send((str(i[1])).encode(FORMAT))
            if count == 0:
                conn.send(str(GAME[0][1]).encode(FORMAT))
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
