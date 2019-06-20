# CamJam EduKit 3 - Robotics
# Worksheet 8 - Line Following Robot
from time import sleep
import time  # Import the Time library
from gpiozero import Robot, LineSensor, Button  # Import the GPIO Zero Library

# Set variables for the line detector GPIO pin
pinLineFollowerLeft = 11
pinLineFollowerRight = 12
pinLineFollowerCenter = 26

# Easier to think the line sensor as a button
linesensorcenter = Button(pinLineFollowerCenter)
linesensorleft = Button(pinLineFollowerLeft)
linesensorright = Button(pinLineFollowerRight)

robot = Robot(left=(23,22), right=(18,17))

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.3
rightmotorspeed = 0.3

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorright = (-leftmotorspeed, rightmotorspeed)
motorleft = (leftmotorspeed, -rightmotorspeed)

def iscenteroverblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linesensorcenter.is_pressed

def isrightoverblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linesensorright.is_pressed

def isleftoverblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linesensorleft.is_pressed

tempo = 0.05
try:
    # repeat the next indented block forever
    robot.value = motorforward
    while True:
        if iscenteroverblack():
            robot.value= motorforward
        #    sleep(tempo)
        if isrightoverblack():
            robot.value= motorright
        #    sleep(tempo)
        if isleftoverblack():
            robot.value= motorleft
        #    sleep(tempo)

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()
