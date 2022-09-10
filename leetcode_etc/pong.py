# Pong
# But non-object oriented

import random
import os
import turtle # Simple graphics, or pygame (requires installation)

wn = turtle.Screen()
wn.title("Pong Pong by @akj")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0) # Stops updating

# Paddle A
pA = turtle.Turtle()
pA.speed(0)
pA.shape("square")
pA.color("white")
pA.shapesize(stretch_wid=5, stretch_len=1)
pA.penup() # Does not need a line
pA.goto(-355, -5)

# Net A
netA = turtle.Turtle()
netA.speed(0)
netA.shape("square")
netA.color("white")
netA.shapesize(stretch_wid=32, stretch_len=0.2)
netA.penup() # Does not need a line
netA.goto(-395, 0)

# Paddle B
pB = turtle.Turtle()
pB.speed(0)
pB.shape("square")
pB.color("white")
pB.shapesize(stretch_wid=5, stretch_len=1)
pB.penup() # Does not need a line
pB.goto(345, -5)

# Net B
netB = turtle.Turtle()
netB.speed(0)
netB.shape("square")
netB.color("white")
netB.shapesize(stretch_wid=32, stretch_len=0.2)
netB.penup() # Does not need a line
netB.goto(386, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup() # Does not need a line
ball.goto(-5, -5)
ball.dx = 2
ball.dy = 2
score_flash = 0

# Pen for scores
score_A = 0
score_B = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)

# Functions
def pA_up():
    y = pA.ycor()
    if y < 240:
        y += 20
        pA.sety(y)
def pA_down():
    y = pA.ycor()
    if y > -240:
        y -= 20
        pA.sety(y)
def pB_up():
    y = pB.ycor()
    if y < 240:
        y += 20
        pB.sety(y)
def pB_down():
    y = pB.ycor()
    if y > -240:
        y -= 20
        pB.sety(y)
def rand_start():
    ball.goto(-5, random.choice(range(-250, 255, 2)))
    ball.dx *= [-1,1][random.randrange(2)]
    ball.dy *= [-1,1][random.randrange(2)]
def write_score():
    pen.clear()
    pen.write("Player A: {} Player B: {}".format(score_A, score_B), align="center", font=("Courier", 24, "normal"))
def bounce():
    os.system("afplay bounce.wav &") 

write_score()
rand_start()
wn.listen()
wn.onkeypress(pA_up, "w")
wn.onkeypress(pA_down, "s")
wn.onkeypress(pB_up, "Up")
wn.onkeypress(pB_down, "Down")

# main game loop
while True:
    wn.update()
    
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    
    # Border checking
    if ball.ycor() > 285:
        ball.sety(285)
        ball.dy *= -1
        bounce()
    if ball.ycor() < -280:
        ball.sety(-280)
        ball.dy *= -1
        bounce()
        
    # Score
    if ball.xcor() > 385:
        bounce()
        # print("Score A")
        score_A += 1
        # ball.setx(385)
        rand_start()
        ball.dx *= -1
        netB.color("red")
        score_flash = 50
        write_score()
    if ball.xcor() < -390:
        bounce()
        # print("Score B")
        score_B += 1
        # ball.setx(-390)
        rand_start()
        ball.dx *= -1
        netA.color("red")
        score_flash = 50
        write_score()
        
        
    # Batting
    if ball.xcor() in range(-345, -335) and (ball.ycor() in range(pA.ycor()-45, pA.ycor()+55)) and ball.dx < 0:
        bounce()
        ball.dx *= -1
        # print("Bat A")
        
    if ball.xcor() in range(330,340) and (ball.ycor() in range(pB.ycor()-45, pB.ycor()+55)) and ball.dx > 0:
        bounce()
        ball.dx *= -1
        # print("Bat B")
        
    if score_flash > 0:
        score_flash -= 1
    else:
        netA.color("white")
        netB.color("white")