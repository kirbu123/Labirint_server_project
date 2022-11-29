import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'

SERVER = '192.168.43.239'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("CONNECTED")


import time
import turtle
from random import randint, choice, randrange

import pygame
# music module
file = 'Dubsleep.mp3'
pygame.init()
pygame.mixer.init()
Music = pygame.mixer.Sound(file)
Music.play(-1)
# music module'''

# screen generation module
screen = turtle.Screen()
screen.title('Labirint game')
screen.bgcolor('black')
screen.setup(620, 620)
screen.tracer(0)
# screen generation module


# labirint maker
grid = []  # boarders array
field = []  # free poles array (places of gaemer motion)


def Board(grid, gamer):  # this is function of detecting, that gamer is in the board place
    for item in grid:
        if gamer.distance(item) < 10 and item.color()[0] == 'white':
            return True
    return False


def Board_index(grid, gamer):  # this is function of detecting and returning index of the board, where gamer is located
    for i in range(len(grid)):
        if gamer.distance(grid[i]) < 10 and grid[i].color()[0] == 'white':
            return i
    return False


def Make_grid(IsBuild=False):  # function of making labirint boarders with updating main params
    global grid, field
    if IsBuild:
        x = -320
        y = 280
        i = False
        while (y > -300):
            if i == True:
                i = False
            else:
                i = True
            while (x < 280):
                if (x ** 2 + y ** 2 != 0):
                    cube = turtle.Turtle()
                    cube.color('white')
                    cube.shape('square')
                    cube.shapesize(0.7, 0.7, 1)
                    cube.penup()
                    cube.goto(x, y)
                    grid.append(cube)
                if i:
                    x += 20
                else:
                    x += 40
            y -= 20
            if i:
                x = -300
            else:
                x = -320

        # algorithm of KRUSKAL (making labirint algorithm) start
        x = -280
        y = 260
        while (y > -300):
            while (x < 280):
                cube = turtle.Turtle()
                cube.hideturtle()
                cube.penup()
                cube.goto(x, y)
                field.append([cube])
                x += 40
            x = -280
            y -= 40

    def Find(a, b):
        global field
        mas = [-1, -1]
        for i in range(len(field)):
            if a in field[i]:
                mas[0] = i
            if b in field[i]:
                mas[1] = i
        return mas

    def Merge(left, right):
        global field
        for i in field[right]:
            field[left].append(i)
        field.pop(right)

    def Find_obj(obj):
        global field
        for i in range(len(field)):
            for j in range(len(field[i])):
                if obj.distance(field[i][j]) < 10:
                    return i
        return -1

    def FindBlocks(obj):
        global grid, field
        build = turtle.Turtle()
        build.hideturtle()
        build.penup()
        build.goto(obj.position()[0], obj.position()[1])
        for i in range(2):
            res = []
            build.setheading(i * 90)
            build.forward(20)
            x = Find_obj(build)
            if x == -1:
                build.forward(-20)
                continue
            res.append(x)
            build.forward(-40)
            x = Find_obj(build)
            if x == -1:
                build.forward(20)
                continue
            res.append(x)
            # build.reset()
            return res
        # build.reset()
        return []

    while (len(field) > 1):
        index = randint(0, len(grid) - 1)
        obj = grid[index]
        mas = FindBlocks(obj)
        #flag = True
        if len(mas) <= 1 or mas[0] == mas[1]:
            continue
        cube = turtle.Turtle()
        cube.hideturtle()
        cube.penup()
        cube.goto(obj.position()[0], obj.position()[1])
        field[mas[0]].append(cube)
        Merge(mas[0], mas[1])
        obj.color('black')
    for i in field[0]:
        flag = True
        for item in grid:
            if i.distance(item) < 10:
                flag = False
                break
        if flag:
            field.append([i])
    field.pop(0)

    # algorithm of KRUSKAL (making labirint algorithm) end


# labirint maker

Make_grid(True)


def Update_gamer():
    global players
    cols = ['yellow', 'blue']  # array of colors of turtles
    for i in range(len(players)):
        players[i].color(cols[i])
        players[i].shape('turtle')
        players[i].shapesize(1, 1, 1)
        players[i].penup()
        players[i].goto(-280, 260)


pcount = 2  # count of players (we have just 2)
players = []  # array of gamer-turtle objects
for i in range(pcount):
    players.append(turtle.Turtle())

Update_gamer()


RunWhile = True


def Stop():
    globals()['screen'].bgcolor('red')
    time.sleep(0.5)
    globals()['RunWhile'] = False


def PlaceBack():
    global players
    for i in players:
        i.goto(-280, 260)



def Clear():
    global grid
    for item in grid:
        item.color('white')


def Update_win():
    global win
    win.goto(240, -260)


win = turtle.Turtle()
win.color('red')
win.shape('turtle')
win.shapesize(1, 1, 1)
win.penup()
Update_win()

# star creating-deleting module---------------------------------
star_obj = []
mas_color = ['red', 'white', 'orange', 'blue', 'yellow']

StarClock = time.time()

StarBoard = 5  # time-board of switching stars

StarCount = 20  # count of all stars


def Make_star():
    global star_obj, StarCount, mas_color, StarClock, win
    for i in range(StarCount):
        x = turtle.Turtle()
        x.shape('square')
        x.shapesize(0.3, 0.3, 1)
        x.setheading(45)
        x.penup()
        x.goto(randrange(-290, 290, 20), randrange(-290, 290, 20))
        star_obj.append(x)
    for i in star_obj:
        i.color(choice(mas_color))
    Update_win()
    StarClock = time.time()


def Update_star():
    global star_obj, StarCount, mas_color, StarClock, win
    for i in star_obj:
        i.goto(randrange(-290, 290, 20), randrange(-290, 290, 20))
    for i in star_obj:
        i.color(choice(mas_color))
    Update_win()
    StarClock = time.time()


Make_star()

# star creating-deleting module---------------------------------
# main updating module

def Move(gamer, grid, dir):
    if dir == "Up" and gamer.position()[1] < 280:
        gamer.setheading(90)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(270)
            gamer.forward(20)
    if dir == "Down" and gamer.position()[1] > -280:
        gamer.setheading(270)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(90)
            gamer.forward(20)
    if dir == "Left" and gamer.position()[0] > -300:
        gamer.setheading(180)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(0)
            gamer.forward(20)
    if dir == "Right" and gamer.position()[0] < 280:
        gamer.setheading(0)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(180)
            gamer.forward(20)

LEN_GRIG = 659
SETGRID_MESSAGE = '!SETGRID'


def Get(conn):
    msg = conn.recv(2048).decode(FORMAT)
    return msg.split()


def Set(conn, msg):
    conn.send(' '.encode(FORMAT))
    conn.send(msg.encode(FORMAT))
    conn.send(' '.encode(FORMAT))

def Send(msg):
    Set(client, msg)
    command = Get(client)
    print(command)
    for iter in range(len(command)):
        if command[iter][0].islower():
            print("FLAG")
            for i in range(LEN_GRIG):
                if command[iter][i] == 'w':
                    grid[i].color('white')
                else:
                    grid[i].color('black')
        else:
            print('move')
            Move(players[1], grid, command[iter])


#grid_sending module (to server)
def Send_grid():
    global grid, client
    s = ''
    for i in range(len(grid)):
        s += grid[i].color()[0][0]
    Set(client, s)

#grid_sending module (to server)

def Move_send(gamer, grid, dir):
    if dir == "Up" and gamer.position()[1] < 280:
        gamer.setheading(90)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(270)
            gamer.forward(20)
        Send("Up")
    if dir == "Down" and gamer.position()[1] > -280:
        gamer.setheading(270)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(90)
            gamer.forward(20)
        Send("Down")
    if dir == "Left" and gamer.position()[0] > -300:
        gamer.setheading(180)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(0)
            gamer.forward(20)
        Send("Left")
    if dir == "Right" and gamer.position()[0] < 280:
        gamer.setheading(0)
        gamer.forward(20)
        if Board(grid, gamer):
            gamer.setheading(180)
            gamer.forward(20)
        Send("Right")


#keys_listening module
screen.onkeypress(lambda: Move_send(players[0], grid, 'Up'), 'Up')
screen.onkeypress(lambda: Move_send(players[0], grid, 'Down'), 'Down')
screen.onkeypress(lambda: Move_send(players[0], grid, 'Left'), 'Left')
screen.onkeypress(lambda: Move_send(players[0], grid, 'Right'), 'Right')

'''
screen.onkeypress(lambda: Move(players[1], grid, 'Up'), 'w')
screen.onkeypress(lambda: Move(players[1], grid, 'Down'), 's')
screen.onkeypress(lambda: Move(players[1], grid, 'Left'), 'a')
screen.onkeypress(lambda: Move(players[1], grid, 'Right'), 'd')
'''

screen.onkeypress(lambda: players[0].goto(-300, 300), 'Z')
screen.onkeypress(lambda: PlaceBack(), 'O')
screen.onkeypress(lambda: players[1].goto(-300, 300), 'V')

screen.onkeypress(lambda: Stop(), 'Q')

screen.listen()
#keys_listening module

#Send_grid()
while RunWhile:
    if time.time() - StarClock > StarBoard:
        Update_star()
    #Send(str(players[0].position()))
    for i in range(len(players)):
        if players[i].distance(win) < 15:
            screen.bgcolor(('yellow', 'blue')[i])
            time.sleep(0.5)
            Clear()
            Make_grid()
            Update_gamer()
            screen.bgcolor('black')
            Update_win()
            Send_grid()
    screen.update()

client.close()
# THE END
