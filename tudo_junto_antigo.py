from gpiozero import Servo
import time
import pigpio
from gpiozero import DistanceSensor
from gpiozero import Robot, Button  # Import the GPIO Zero Library

# Set variables for the line detector GPIO pins
pinLineFollowerLeft = 11 #23
pinLineFollowerRight = 12 #32
pinLineFollowerCenter = 26 #37

# Set variables for US and servo GPIO pins
pinServo = 19 #35
pinEcho = 16 #36
pinTrig = 13 #33

# Easier to think the line sensor as a button
linesensorcenter = Button(pinLineFollowerCenter)
linesensorleft = Button(pinLineFollowerLeft)
linesensorright = Button(pinLineFollowerRight)

# Set motors pins
robot = Robot(left=(23,22), right=(18,17)) # azul verde preto branco

# Inicialize servo motor
myCorrection=0.45
maxPW=(2.0+myCorrection+0.01)/1000
minPW=(1.0-myCorrection)/1000
servo = Servo(pinServo,min_pulse_width=minPW,max_pulse_width=maxPW)

#Inicialize distance sensor
pi = pigpio.pi()

pi.set_mode(pinTrig, pigpio.OUTPUT)
pi.set_mode(pinEcho, pigpio.INPUT)
pi.set_pull_up_down(pinEcho, pigpio.PUD_DOWN)

if not pi.connected:
    exit()

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.3
rightmotorspeed = 0.3

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorright = (-leftmotorspeed, rightmotorspeed)
motorleft = (leftmotorspeed, -rightmotorspeed)

# Starts servo at min position
servo_position = -0.9
servo.value = servo_position
robotlost = False
time.sleep(1)

###############################################################################
#Teste Servo

# while True:
#     servo.value = 0
#     print("mid")
#     time.sleep(0.5)
#     servo.value = -1
#     print("min")
#     time.sleep(1)
#     servo.value = 0
#     print("mid")
#     time.sleep(0.5)
#     servo.value = 1
#     print("max")
#     time.sleep(1)

################################################################################
#Teste US

# try:
#     while True:
#         print('Distance: ', sensor.distance * 100)

################################################################################

def sensor.distance:
    endtime = 0
    #print('aqui')
    pi.write(pinTrig, 0)
    time.sleep(2/1000000)
    pi.write(pinTrig, 1)
    time.sleep(10/1000000)
    pi.write(pinTrig, 0)
    starttime = time.time()

    while (pi.read(pinEcho) == 0):
        starttime = time.time()
    #    print("preso aqui")
    while (pi.read(pinEcho) == 1):
        endtime = time.time()
    duration = endtime - starttime
    distance = (duration*0.034*1000000/(2))

    return distance

def iscenteroverblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linesensorcenter.is_pressed

def isrightoverblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linesensorright.is_pressed

def isleftoverblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linesensorleft.is_pressed

def seekobstacle():
    global robotlost, servo_position
    robot.stop()
    starttime2 = time.time()
    direction = 0.05

    while ((sensor.distance*100) > 40) and not robotlost:
        if ((time.time() - starttime2) < 5.0):
            if (servo_position < -0.95 and direction == -0.05) or (servo_position > 0.95 and direction == 0.05):
                direction = -direction
            servo_position += direction
            servo.value = servo_position
            time.sleep(0.03)
            robotlost = False
        else:
            robotlost = True
    return servo_position

try:
    # Starts motor forward
    diminui_velocidade = True
    while not (iscenteroverblack() and isrightoverblack() and isleftoverblack()) and not robotlost:
        if (sensor.distance > 20):
        #     print(sensor.distance)
        #     if (sensor.distance < 30):# and diminui_velocidade:
        #         print("diminuindo velocidade "+str(sensor.distance))
                #motorforward = (leftmotorspeed-0.15, rightmotorspeed-0.15)
                #motorbackward = (-leftmotorspeed+0.15, -rightmotorspeed+0.15)
                #motorright = (-leftmotorspeed+0.15, rightmotorspeed-0.15)
                #motorleft = (leftmotorspeed-0.15, -rightmotorspeed+0.15)
                #robot.stop()
                #time.sleep(1)
                #diminui_velocidade = False
            if iscenteroverblack():
                print("para frente")
                robot.value = motorforward
            #    time.sleep(tempo)
            if isrightoverblack():
                print("para a direita")
                robot.value = motorright
            #    time.sleep(tempo)
            if isleftoverblack():
                print("para a esquerda")
                robot.value = motorleft
            #    time.sleep(tempo)
        else:
            print("achou objeto")
            servo_position = 0
            servo.value = servo_position
            time.sleep(1)
            robot.value = motorright
            time.sleep(0.8)
            while (sensor.distance) > 30:

                print('vira ' +  str(sensor.distance))
                robot.value = motorright
                time.sleep(0.5)
                robot.stop()

            print('comeca contorno')
            time.sleep(1)
            robot.stop()
            while not iscenteroverblack():
                print(sensor.distance)
                if (sensor.distance) > 40:
                    seekobstacle()
                if sensor.distance > 15 and sensor.distance < 20:
                    robot.value = motorforward
                    time.sleep(0.5)
                    robot.stop()
                if (sensor.distance) < 15:
                    robot.value = motorleft
                    time.sleep(0.2)
                    robot.value = motorforward
                    time.sleep(0.5)
                    robot.stop()
                if (sensor.distance) > 20:
                    robot.value = motorright
                    time.sleep(0.2)
                    robot.value = motorforward
                    time.sleep(0.5)
                    robot.stop()
            # # # Starts servo at min position
            servo_position = -0.9
            servo.value = servo_position
    print("acaba?")

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()
