# Snake
# Object oriented

import os
# import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1 # Always going right
        self.dirny = 0
        self.color = color


    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = ( # Counting numbers of columns/rows here
            self.pos[0] + self.dirnx,
            self.pos[1] + self.dirny
            )

    def draw(self, surface, eyes=False): # Draw eyes if True
        dist = self.w // self.rows
        i = self.pos[0] # row
        j = self.pos[1] # col

        # Cube
        pygame.draw.rect(
            surface,
            self.color,
            (i*dist+1, j*dist+1, dist-1, dist-1) # Not covering the grid lines
            )
        # Eyes, if True
        if eyes:
            centre = dist // 2
            radius = 2
            circleMiddle1 = (i*dist+centre-radius, j*dist+8)
            circleMiddle2 = (i*dist+dist-radius*2, j*dist+8)
            pygame.draw.circle(surface, (255,255,255), circleMiddle1, radius)
            pygame.draw.circle(surface, (255,255,255), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {} # Dictionary of head position, to directions changed

    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.head = Cube(self.pos)
        self.body.append(self.head)
        self.dirnx = 0 # Direction x
        self.dirny = 1 # Direction y

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # First thing to check is quit
                pygame.quit()
            keys = pygame.key.get_pressed() # Multiple key presses accepted

            # In pygame, top lefthand corner is (0,0)
            for key in keys: # One key/turn at a time!
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]  # Dictionary addition
                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]  # Dictionary addition
                elif keys[pygame.K_UP] and self.dirny != 1: # Y is inverted from standard flow
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]  # Dictionary addition
                elif keys[pygame.K_DOWN] and self.dirny != -1: # Y is inverted from standard flow
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]  # Dictionary addition

        for i, c in enumerate(self.body):
            p = c.pos[:] # Copies exact position
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1: # If trailing snake body longer than length
                    self.turns.pop(p) # Remove body position
            else: # Check if crossing the edge of board
                if c.dirnx == -1 and c.pos[0] <= 0: # Clipping left
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: # Clipping right
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: # Clipping down
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: # Clipping up
                    c.pos = (c.pos[0], c.rows-1)

                else: # Normal movement
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: # Move right, add left
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        if dx == -1 and dy == 0: # Move left, add right
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        if dx == 0 and dy == 1: # Move down, add up
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        if dx == 0 and dy == -1: # Move up, add down
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(
            surface,
            (55, 55,55), # Grey
            (x,0), # Start position
            (x,w) # End position
            )
        pygame.draw.line(
            surface,
            (55, 55,55), # Grey
            (0,y), # Start position
            (w,y) # End position
            )

def redrawWindow(surface): # Redraw window
    global rows, width, s, snack
    surface.fill((0, 0, 0)) # Black background
    s.draw(surface) # draw snake
    snack.draw(surface) # draw snack
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue # Continue loop
        else:
            break # Break loop and return (x, y)

    return (x, y)

def messageBox(subject, content): # Useful popup window system
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def bounce(): # Make bounce sound; sourced from Pong
    os.system("afplay bounce.wav &")

def main():
    global rows, width, s, snack
    rows = 20
    width = 500
    win = pygame.display.set_mode((width, width))
    s = Snake(
        (255, 0, 0), # Red
        (10,10)
        )
    snack = Cube(
        randomSnack(rows, s),
        color=(0,255,0) # Green snack
        )
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50) # 50 miliseconds delay
        clock.tick(10) # Max 10 blocks in 1 sec

        s.move()

        if s.body[0].pos == snack.pos: # Snack eaten
            s.addCube()
            snack = Cube(randomSnack(rows,s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score ', len(s.body))
                messageBox('You lost!', 'Play again!')
                s.reset((10, 10))
                break

        redrawWindow(win)

    pass

main()
