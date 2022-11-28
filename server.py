import socket
import threading

HEADER = 64
PORT = 5050
LEN_GRIG = 659
SERVER = '192.168.31.151' #socket.gethostbyname(socket.gethostname()) #'172.29.16.1'


ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT = 'utf-8'
DISCONNECTED_MESSAGE = '!DISCONNECT'
SETGRID_MESSAGE = '!SETGRID'
GAME = []

def handle_client(conn, addr):
    global GAME
    GAME.append(conn)
    print('NEW_CONNECTION: ' + str(addr) + " connected: ")
    connected = True
    while connected:
        msg_lenght = conn.recv(HEADER).decode(FORMAT)
        if msg_lenght:
            msg_lenght = int(msg_lenght)
            msg = conn.recv(msg_lenght).decode(FORMAT)


            this, other = GAME[0], GAME[1]
            for i in range(len(GAME)):
                if GAME[i][0] != conn:
                    other = GAME[i]
                else:
                    this = GAME[i]


            if msg == DISCONNECTED_MESSAGE:
                connected = False
                continue
            elif msg == SETGRID_MESSAGE:
                if len(GAME) == 1:
                    continue
                other.send('!SETGRID')
                for i in range(LEN_GRIG):
                    msg_lenght = conn.recv(HEADER).decode(FORMAT)
                    if msg_lenght:
                        msg_lenght = int(msg_lenght)
                        msg = conn.recv(msg_lenght).decode(FORMAT)
                        other.send(msg.encode(FORMAT))
                continue

            print(str(addr) + ' SENT: ' + str(msg))
            count = 0


            if len(GAME) == 1:
                this.send(msg.encode(FORMAT))
            else:
                other.send(msg.encode(FORMAT))

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
