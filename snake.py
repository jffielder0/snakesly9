#!/usr/bin/env python3

# noobtuts.com/python/snake-game
# requires pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL._bytes import as_8_bit # reads ascii keystrokes as octal

from random import randint


window = 0                                             # glut window number
width, height = 500, 500                               # window size
field_width, field_height = 50, 50                     # internal resolution
snake = [(20, 20)] # snake list of (x, y) positions
snake_dir = (1, 0)  # snake movement direction
interval = 100 # update interval in milliseconds
food = [] # food list of type (x, y)


def draw_snake():
    glColor3f(1.0, 1.0, 1.0)  # set color to white
    for x, y in snake:        # go through each (x, y) entry
        draw_rect(x, y, 1, 1) # draw it at (x, y) with width=1 and height=1

def draw_food():
    glColor3f(0.5, 0.5, 1.0)  # set color to blue
    for x, y in food:         # go through each (x, y) entry
        draw_rect(x, y, 1, 1) # draw it at (x, y) with width=1 and height=1


def refresh2d_custom(width, height, internal_width, internal_height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, internal_width, 0.0, internal_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)                                  # start drawing a rectangle
    glVertex2f(x, y)                                   # bottom left point
    glVertex2f(x + width, y)                           # bottom right point
    glVertex2f(x + width, y + height)                  # top right point
    glVertex2f(x, y + height)                          # top left point
    glEnd()                                            # done drawing a rectangle

def draw():                                            # draw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d_custom(width, height, field_width, field_height)

    draw_food()
    draw_snake()
    glutSwapBuffers()                                  # important for double buffering

def update(value):
    # move snake
    print (snake)
    snake.insert(0, vec_add(snake[0], snake_dir))      # insert new position in the beginning of the snake list
    snake.pop()                                        # remove the last element

    # spawn food
    r = randint(0, 20)                                 # spawn food with 5% chance
    if r == 0:
        x, y = randint(0, field_width), randint(0, field_height) # random spawn pos
        food.append((x, y))

    # let the snake eat the food
    (hx, hy) = snake[0]          # get the snake's head x and y position
    for x, y in food:            # go through the food list
        if hx == x and hy == y:  # is the head where the food is?
            snake.append((x, y)) # make the snake longer
            food.remove((x, y))  # remove the food


    glutTimerFunc(interval, update, 0)                 # trigger next update

def vec_add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])



def keyboard(*args):
    w_key = as_8_bit('\167')
    a_key = as_8_bit('\141')
    s_key = as_8_bit('\163')
    d_key = as_8_bit('\144')
    global snake_dir                                   # important if we want to set it to a new value
    arg_trans = args[0]
    print (arg_trans)
    if args[0] == w_key :
        snake_dir = (0, 1)                             # up
    if args[0] == s_key:
        snake_dir = (0, -1)                            # down
    if args[0] == a_key:
        snake_dir = (-1, 0)                            # left
    if args[0] == d_key:
        snake_dir = (1, 0)                             # right


# initialization
glutInit()                                             # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(0, 0)                           # set window position
window = glutCreateWindow("Snake AI Project")              # create window with title
glutDisplayFunc(draw)                                  # set draw function callback
glutIdleFunc(draw)                                     # draw all the time
glutTimerFunc(interval, update, 0)                     # trigger next update
glutKeyboardFunc(keyboard)                             # tell opengl that we want to check keys
glutMainLoop()                                       # start everything
