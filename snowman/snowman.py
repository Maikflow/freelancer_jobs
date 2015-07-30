#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(10 points) In this assignment you will use the `turtle` python module 
to draw a snowman. You may NOT use the Turtle.circle function to draw 
circles.

Snowman description:

The outline of the snowman should be in black.

The snowman’s body should be made of 3 circles.

Each circle should be centered above the one below it 
(except the bottom circle, which can be located anywhere).

There should be no gap between the circles.

Give the snowman eyes, a nose and four buttons (a hat is optional).
you can use the dot() function or stamp() function for eyes and buttons
you can draw a small triangle (or dot) for the nose
you should increase the width of turtle before using the dot function. use the width() function to set the width of turtle.


Optional parts (not required, but can get you two bonus points if done):

The snowman should be on a blue background, and should be drawn filled with white.
You can include two stick-arms and at least two fingers on each hand.
Draw some trees, simply draw green triangle with brown rectangle as stem.
Coloring of different items: buttons, eyes, nose, hat.
"""

import turtle 
import Tkinter as tk

def draw_snowman(snowman, initial_position=[100,100]):
    """Draw a complete snowman (eyes,hat,nose,buttons,arms) and a tree"""

    #Build the window 
    root = tk.Tk()
    root.geometry('500x500-5+40')
    cv = turtle.ScrolledCanvas(root, width=900, height=900)
    cv.pack()
    
    #Paint the background
    scr = turtle.TurtleScreen(cv)
    scr.bgcolor('#BFE2FF')

    #Initialize the Turtle, put it in canvas
    snowman = turtle.RawTurtle(scr)
    start = initial_position

    #Draw the 3 circles
    snowman.pen(fillcolor='white')
    for i in range(3):
        snowman.penup()
        snowman.goto(initial_position)
        snowman.pd()
        snowman.begin_fill()

        while True:
            snowman.left(2)
            snowman.forward(1)
            if int(snowman.heading()) == 180:
                diameter = snowman.pos()[1] - initial_position[1]
            if int(snowman.heading()) == 0:
                break
        snowman.end_fill()
        initial_position[1] += diameter

    #Draw the hat
    snowman.pu()
    snowman.goto(initial_position)
    snowman.pd()
    snowman.pen(fillcolor='purple')
    snowman.seth(0)
    snowman.begin_fill()
    snowman.forward(0.5*diameter)
    snowman.left(90)
    snowman.forward(0.2*diameter)
    snowman.left(90)
    snowman.forward(0.25*diameter)
    snowman.right(90)
    snowman.forward(0.5*diameter)
    snowman.left(90)
    snowman.forward(0.5*diameter)
    snowman.left(90)
    snowman.forward(0.5*diameter)
    snowman.right(90)
    snowman.forward(0.25*diameter)
    snowman.left(90)
    snowman.forward(0.2*diameter)
    snowman.left(90)
    snowman.forward(0.5*diameter)
    snowman.end_fill()
    snowman.pu()
 
    #Draw the buttons
    initial_position[1] -= diameter
    snowman.width(5)
    for i in range(4):
        initial_position[1] -= 0.2*diameter
        snowman.goto(initial_position)    
        snowman.dot(6,'green')
    initial_position[1] += 2*diameter

    #Draw the nose 
    snowman.pen(fillcolor='orange')
    initial_position[1] -= 0.7*diameter
    snowman.right(90)
    snowman.goto(initial_position)
    snowman.stamp()

    #Draw the eyes
    initial_position[0] += 0.25*diameter
    initial_position[1] += 0.25*diameter
    snowman.goto(initial_position)
    snowman.width(5)
    snowman.dot(10,'grey')
    initial_position[0] -= 0.5*diameter
    snowman.goto(initial_position)
    snowman.dot(10,'grey')

    #Draw the stick arms and fingers
    initial_position[0] -= 0.25*diameter
    initial_position[1] -= 1.25*diameter
    right_stick = [initial_position[0]+diameter,initial_position[1]]
    snowman.goto(initial_position)
    snowman.seth(135)
    snowman.width(2)
    snowman.pd()
    snowman.forward(diameter/2)
    snowman.backward(diameter/7)
    snowman.seth(235)
    snowman.forward(diameter/7)
    snowman.backward(2*diameter/7)
    snowman.pu()
    snowman.goto(right_stick)
    snowman.pd()
    snowman.seth(45)
    snowman.width(2)
    snowman.pd()
    snowman.forward(diameter/2)
    snowman.backward(diameter/7)
    snowman.seth(135)
    snowman.forward(diameter/7)
    snowman.backward(2*diameter/7)

    #Draw the tree
    snowman.pu()
    start[0] -= 2*diameter
    start[1] -= diameter
    snowman.goto(start)
    snowman.seth(90)
    snowman.shape('triangle')
    snowman.shapesize(6,6,2)
    snowman.pen(fillcolor='brown')
    snowman.stamp()
    snowman.goto(start[0],start[1]+60)
    snowman.pen(fillcolor='green')
    snowman.stamp()
    root.mainloop()

if __name__ == "__main__":
    draw_snowman(0, [10,0])
    

