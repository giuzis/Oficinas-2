# CamJam EduKit 3 - Robotics
# Worksheet 8 - Line Following Robot
from time import sleep
from gpiozero import Robot # Import the GPIO Zero Library

robot = Robot(left=(23,22), right=(18,17))

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.6
rightmotorspeed = 0.6

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorleft = (-leftmotorspeed, rightmotorspeed)
motorright = (leftmotorspeed, -rightmotorspeed)


try:
    # repeat the next indented block forever
    robot.value = motorforward
    while True:
        robot.value = motorforward

        sleep(1)
        robot.value = motorright
        sleep(1)
        robot.value = motorleft
        sleep(1)

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()
