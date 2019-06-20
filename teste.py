# CamJam EduKit 3 - Robotics
# Worksheet 5 - Line Detection

import time  # Import the Time library
from gpiozero import LineSensor  # Import the GPIO Zero Library

# Set variables for the GPIO pins
pinLineFollowerFront = 11
pinLineFollowerBack = 9

sensorFront = LineSensor(pinLineFollowerFront)
sensorBack = LineSensor(pinLineFollowerBack)


# Define the functions that will be called when the line is
# detected or not detected
def lineseenfront():
    print("Line seen front")


def linenotseenfront():
    print("No line seen front")

def lineseenback():
    print("Line seen back")


def linenotseenback():
    print("No line seen back")


# Tell the program what to do with a line is seen
sensorFront.when_line = linenotseenfront
# And when no line is seen
sensorFront.when_no_line = lineseenfront

# Tell the program what to do with a line is seen
sensorBack.when_line = linenotseenback
# And when no line is seen
sensorBack.when_no_line = lineseenback

try:
    # Repeat the next indented block forever
    while True:
        time.sleep(10)

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    print("Exiting")