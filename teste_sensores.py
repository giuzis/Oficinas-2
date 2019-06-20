import time  # Import the Time library
from time import sleep
from gpiozero import LineSensor  # Import the GPIO Zero Library

# Set variables for the line detector GPIO pin
pinLineFollowerLeft = 11
pinLineFollowerRight = 12

linesensorright = LineSensor(pinLineFollowerRight)
linesensorleft = LineSensor(pinLineFollowerLeft)

rightisoverwhite = True  # A flag to say the robot can see a black line
leftisoverwhite = True  # A flag to say the robot can see a black line
rightlinelost = False  # A flag that is set if the line has been lost
leftlinelost = False

# Define the functions that will be called when the line is
# detected or not detected
def blacknotseenright():
    global rightisoverwhite, rightlinelost
    print("Right white.")
    rightisoverwhite = True
    rightlinelost = False

def blackseenright():
    global rightisoverwhite
    print("Right black.")
    rightisoverwhite = False

 # Define the functions that will be called when the line is
# detected or not detected
def blacknotseenleft():
    global leftisoverwhite, leftlinelost
    print("Left white.")
    leftisoverwhite = True
    leftlinelost = False

def blackseenleft():
    global leftisoverwhite
    print("Left black.")
    leftisoverwhite = False

# Search for the white
def seekwhiteleft():
    global leftlinelost

    print("Seek white left")

    seektime = 0.25  # Turn for 0.25s
    seekcount = 1  # A count of times the robot has looked for the line
    maxseekcount = 10  # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or we have looked long enough
    while seekcount <= maxseekcount:

        # Save the time it is now
        starttime = time.time()

        # While the robot is turning for seektime seconds,
        # check to see whether the line detector is over black
        while (time.time() - starttime) <= seektime:
            if leftisoverwhite:
                # Exit the seekline() function returning
                # True - the line was found
                print("Left found")
                return True

        # Increase the seek count
        seekcount += 1

    print("Left lost.")
    leftlinelost = True
    return False

# Search for the white
def seekwhiteright():
    global rightlinelost

    print("Seek white right")

    seektime = 0.25  # Turn for 0.25s
    seekcount = 1  # A count of times the robot has looked for the line
    maxseekcount = 10  # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or we have looked long enough
    while seekcount <= maxseekcount:

        # Save the time it is now
        starttime = time.time()

        # While the robot is turning for seektime seconds,
        # check to see whether the line detector is over black
        while (time.time() - starttime) <= seektime:
            if rightisoverwhite:
                # Exit the seekline() function returning
                # True - the line was found
                print("Right found")
                return True

        # Increase the seek count
        seekcount += 1

    print("Right lost.")
    rightlinelost = True
    return False

# Tell the program what to do with a white line is seen
linesensorright.when_line = blacknotseenright
# And when no line is seen
linesensorright.when_no_line = blackseenright


# Tell the program what to do with a white line is seen
linesensorleft.when_line = blacknotseenleft
# And when no line is seen
linesensorleft.when_no_line = blackseenleft

try:
    while True:
        if not rightisoverwhite and not rightlinelost:
            seekwhiteright()
            sleep(0.1)
        if not leftisoverwhite and not leftlinelost:
            seekwhiteleft()
            sleep(0.1)


# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()