# CamJam EduKit 3 - Robotics
# Worksheet 8 - Line Following Robot
from time import sleep
import time  # Import the Time library
from gpiozero import Robot, LineSensor, Button  # Import the GPIO Zero Library

# Set variables for the line detector GPIO pin
pinLineFollowerLeft = 11
pinLineFollowerRight = 12
pinLineFollowerCenter = 26

linesensorcenter = Button(pinLineFollowerCenter)
linesensorleft = Button(pinLineFollowerLeft)
linesensorright = Button(pinLineFollowerRight)

robot = Robot(left=(23,22), right=(18,17))

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.7
rightmotorspeed = 0.7

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorright = (leftmotorspeed, -rightmotorspeed)
motorleft = (-leftmotorspeed, rightmotorspeed)

direction = True  # The direction the robot will turn - True = Left
isoverblack = True  # A flag to say the robot can see a black line
linelost = False  # A flag that is set if the line has been lost


# Define the functions that will be called when the line is
# detected or not detected
def lineseen():
    global isoverblack, linelost
    #print("The line has been found.")
    isoverblack = True
    linelost = False


def linenotseen():
    global isoverblack
    #print("The line has been lost.")
    isoverblack = False


# Search for the black line
def seekline():
    global direction, linelost
    robot.stop()

    print("Seeking the line")

    change_direction = 0
    seeksize = 0.25  # Turn for 0.25s
    seekcount = 1  # A count of times the robot has looked for the line
    maxseekcount = 5  # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or we have looked long enough
    while seekcount <= maxseekcount:
        # Set the seek time
        seektime = seeksize * seekcount

        if not linesensorleft.is_pressed and linesensorright.is_pressed:
            print("Looking left")
            robot.value = motorleft
        elif linesensorleft.is_pressed and not linesensorright.is_pressed:
            print("Looking Right")
            robot.value = motorright
        else:
            print("Looking black")
            robot.value = motorforward
            seektime = seeksize/2

        # Start the motors turning in a direction
        if direction:
            print("Looking left")
            robot.value = motorleft
        else:
            print("Looking Right")
            robot.value = motorright

        # Save the time it is now
        starttime = time.time()

        # While the robot is turning for seektime seconds,
        # check to see whether the line detector is over black
        while (time.time() - starttime) <= seektime:
            if linesensorcenter.is_pressed:
                linenotseen()
            else:
                lineseen()
            if isoverblack:
                robot.value = motorforward
                # Exit the seekline() function returning
                # True - the line was found
                return True

        # The robot has not found the black line yet, so stop
        robot.stop()

        # Increase the seek count
        seekcount += 1

        # Change direction
        if change_direction:
            direction = not direction

    # The line wasn't found, so return False
    robot.stop()
    print("The line has been lost - relocate your robot")
    linelost = True
    return False


# Tell the program what to do with a line is seen
#linesensor.when_line = linenotseen
# And when no line is seen
#linesensor.when_no_line = lineseen
tempo = 0.05
try:
    # repeat the next indented block forever
    robot.value = motorforward
    while True:
        #if linesensorcenter.is_pressed:
        #    robot.value= motorforward
            #sleep(tempo)
        if not linesensorcenter.is_pressed:
            robot.value= motorforward
        #    sleep(tempo)
        if not linesensorright.is_pressed:
            robot.value= motorright
        #    sleep(tempo)
        if not linesensorleft.is_pressed:
            robot.value= motorleft
        #    sleep(tempo)
        #if linesensorcenter.is_pressed:
        #    linenotseen()
        #else:
        #    lineseen()
        #if not isoverblack and not linelost:
        #    seekline()


# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()