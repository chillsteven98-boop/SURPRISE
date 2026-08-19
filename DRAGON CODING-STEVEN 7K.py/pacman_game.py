from random import choice
from turtle import *
from freegames import floor,vector

state={"score":0}
path=Turtle(visible=False)
writer=Turtle(visible=False)
effects=Turtle(visible=False)
aim=vector(5,0)
pacman=vector(-40,-80)
ghosts=[
[vector(-180,160),vector(5,0)],
[vector(-180,-160),vector(0,5)],
[vector(100,160),vector(0,-5)],
[vector(100,-160),vector(-5,0)],
]

tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x,y):
    path.up()
    path.goto(x,y)
    path.down()
    path.begin_fill()
    for count in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    x=(floor(point.x,20)+200)/20
    y=(180-floor(point.y,20))/20
    index=int(x+y*20)
    return index

def valid(point):
    index=offset(point)
    if tiles[index]==0:
        return False
    index=offset(point+19)
    if tiles[index]==0:
        return False
    return point.x % 20==0 or point.y % 20==0

def world():
    bgcolor('black')
    path.color('blue')
    for index in range(len(tiles)):
        tile=tiles[index]
        if tile>0:
            x=(index%20)*20-200
            y=180-(index//20)*20
            square(x,y)
            if tile==1:
                path.up()
                path.goto(x+10,y+10)
                path.dot(2,'white')

def move():
    writer.undo()
    writer.write(state['score'])
    clear()
    if valid(pacman+aim):
        pacman.move(aim)
    index=offset(pacman)
    if tiles[index]==1:
        tiles[index]=2
        state['score']+=1
        x=(index%20)*20-200
        y=180-(index//20)*20
        square(x,y)
        eat_animation(x,y,size=12)
    up()
    goto(pacman.x+10,pacman.y+10)
    dot(20,'yellow')
    for point,course in ghosts:
        
        options=[vector(5,0),vector(-5,0),
            vector(0,5),vector(0,-5)]
        if point.x %20==0 and point.y %20==0:
            valid_options=[]
            for option in options:
                if valid(point+option):
                    valid_options.append(option)
            if valid_options:

                plan=min(valid_options,key=lambda option: abs((point+option)-pacman))
                course.x=plan.x
                course.y=plan.y
        if valid(point+course):
            point.move(course)
        up()
        goto(point.x+10,point.y+10)
        dot(20,'red')
    update()
    for point,course in ghosts:
        if abs(pacman-point)<20:
            return
    ontimer(move,100)

def change(x,y):
    if valid(pacman+vector(x,y)):
        aim.x=x
        aim.y=y

def eat_animation(x,y,size=12):
    effects.clear()
    effects.goto(x+10,y+10)
    effects.dot(size,"yellow")
    update()
    if size>2:
        ontimer(lambda:eat_animation(x,y,size-4),30)
    else:
        effects.clear()

setup(420,420,370,0)
hideturtle()
tracer(False)
writer.goto(160,160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda:change(5,0),'Right')
onkey(lambda:change(-5,0),'Left')
onkey(lambda:change(0,5),'Up')
onkey(lambda:change(0,-5),'Down')
world()
move()
done()