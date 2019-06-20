import time
from time import sleep
import warnings
import pigpio
from gpiozero import DistanceSensor
from gpiozero import Robot, Button, Servo  # Import the GPIO Zero Library

warnings.simplefilter('ignore')

# Set variables for the line detector GPIO pins
pinLineFollowerLeft = 11    #23
pinLineFollowerRight = 12   #32
pinLineFollowerCenter = 26  #37
pinLineDetectorLeft = 14     #8
pinLineDetectorRight = 21   #40


# Set variables for US and servo GPIO pins
pinServo = 19 #35
pinEcho = 16 #36
pinTrig = 13 #33

# Easier to think the line sensor as a button
linesensorcenter = Button(pinLineFollowerCenter)
linesensorleft = Button(pinLineFollowerLeft)
linesensorright = Button(pinLineFollowerRight)
linedetectorleft = Button(pinLineDetectorLeft)
linedetectorright = Button(pinLineDetectorRight)

# Set motors pins
robot = Robot(left=(23,22), right=(18,17)) # azul verde preto branco

# Inicialize servo motor
myCorrection=0.45
maxPW=(2.0+myCorrection+0.01)/1000
minPW=(1.0-myCorrection)/1000
servo = Servo(pinServo,min_pulse_width=minPW,max_pulse_width=maxPW)

#Inicialize distance sensor
sensor = DistanceSensor(echo = pinEcho, trigger = pinTrig)
# pi = pigpio.pi()
#
# pi.set_mode(pinTrig, pigpio.OUTPUT)
# pi.set_mode(pinEcho, pigpio.INPUT)
# pi.set_pull_up_down(pinEcho, pigpio.PUD_DOWN)

# if not pi.connected:
#     exit()

# Set the relative speeds of the two motors, between 0.0 and 1.0
leftmotorspeed = 0.2
rightmotorspeed = 0.2

motorforward = (leftmotorspeed, rightmotorspeed)
motorbackward = (-leftmotorspeed, -rightmotorspeed)
motorright = (0, rightmotorspeed)
motorleft = (leftmotorspeed, 0)

# Starts servo at min position
servo_position = -0.9
servo.value = servo_position
robotlost = False
time.sleep(1)

def sensor_distance():
    distance = sensor.distance*100
    # endtime = 0
    #
    # pi.write(pinTrig, 0)
    # time.sleep(2/1000000)
    # pi.write(pinTrig, 1)
    # time.sleep(10/1000000)
    # pi.write(pinTrig, 0)
    # starttime = time.time()
    #
    # while (pi.read(pinEcho) == 0):
    #     starttime = time.time()
    # while (pi.read(pinEcho) == 1):
    #     endtime = time.time()
    # duration = endtime - starttime
    # distance = (duration*0.034*1000000/(2))

    return distance

def return_distance():
    distance = 0
    for i in range(0,100):
        distance = distance + sensor_distance()
    distance = distance/100
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

def isleftdetectingblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linedetectorleft.is_pressed

def isrightdetectingblack():
    # It is 'pressed' if is over white, otherwise is black
    return not linedetectorright.is_pressed

def seekobstacle():
    global robotlost, servo_position
    robot.stop()
    starttime2 = time.time()
    direction = 0.05

    while ((return_distance()) > 25) and not robotlost:
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

directions_vector = [1,0]

try:
    # Starts motor forward
    number_conversion = 0
    contagem_verifica = 0
    distance = 100

    robot.value = motorforward
    while not robotlost:

        #seguidor de linha
        if iscenteroverblack():
            print("para frente")
            robot.value = motorforward
        if isrightoverblack():
            print("para a direita")
            robot.value = motorright
            #movimento_anterior = motorright
        if isleftoverblack():
            print("para a esquerda")
            robot.value = motorleft
            #movimento_anterior = motorleft

        if isrightdetectingblack() or isleftdetectingblack():
            robot.stop()
            if len(directions_vector) == number_conversion:
                robotlost = True
                print("Chegou ao fim")
            elif directions_vector[number_conversion] == 0:     #vira para a direita
                robot.stop()
                time.sleep(0.5)
                print("vira para a direita")
                # robot.value = motorright
                # time.sleep(0.5)
                while isleftdetectingblack() or isrightdetectingblack():
                    if isleftdetectingblack():
                        print("detectando esquerda")
                    if isrightdetectingblack():
                        print("detectando direita")
                    robot.value = motorforward
                while iscenteroverblack():
                    print("procurando branco")
                    robot.value = motorright
                while not iscenteroverblack():
                    print("vira para a direita")
                    robot.value = motorright
                robot.stop()
            else:                                               #vira para a esquerda
                robot.stop()
                time.sleep(0.5)
                print("vira para a esquerda")
                # robot.value = motorleft
                # time.sleep(0.5)
                while isleftdetectingblack() or isrightdetectingblack():
                    if isleftdetectingblack():
                        print("detectando esquerda")
                    if isrightdetectingblack():
                        print("detectando direita")
                    robot.value = motorforward
                while iscenteroverblack() or isrightoverblack() or isleftoverblack():
                    print("procurando branco")
                    robot.value = motorleft
                while not iscenteroverblack() or isleftdetectingblack() or isrightdetectingblack():
                    print("vira para a esquerda")
                    robot.value = motorleft
                robot.stop()
            number_conversion += 1

        # if contagem_verifica > 700:   # a cada contagem igual a 700 o robo para checar a distancia
        #     robot.stop()
        #     time.sleep(0.2)
        #     contagem_verifica = 0
        #     distance = return_distance()
        #     print("distancia " + str(distance))
        #     if not (distance > 25):
        #         print("achou objeto")
        #         servo_position = 0
        #         servo.value = servo_position
        #         time.sleep(1)
        #         while return_distance() > 27:
        # pensar em fazer isso fazendo com que o us foque na parte do objeto que esta mais perto
        # ou seja, gravar a distancia logo que ele encontra o objeto e usa-la para localizar o meio
        # do objeto na hora de virar
        # tentar usar essa mesma distancia na hora de contornar o objeto
        #             robot.value = motorright
        #             time.sleep(0.15)
        #             robot.stop()
        #             time.sleep(0.5)
        #             print("preso aqui")
        #         robot.value = motorforward
        #         time.sleep(0.1)
        #         print('comeca contorno')
        #         robot.stop()
        #         while not iscenteroverblack():
        #             distance = return_distance()
        #             print("fazendo contorno " +str(distance))
        #             if distance > 25:
        #                print("procura obstaculo")
        #                seekobstacle()
        #             if distance > 10 and distance < 20:
        #                 print("para frente")
        #                 robot.value = motorforward
        #                 time.sleep(0.1)
        #                 robot.stop()
        #                 time.sleep(0.5)
        #             if distance < 10:
        #                 print("para direita")
        #                 robot.value = motorright
        #                 time.sleep(0.1)
        #                 robot.value = motorforward
        #                 time.sleep(0.1)
        #                 robot.stop()
        #                 time.sleep(0.5)
        #             if distance > 20:
        #                 print("para esquerda")
        #                 robot.value = motorleft
        #                 time.sleep(0.1)
        #                 robot.value = motorforward
        #                 time.sleep(0.1)
        #                 robot.stop()
        #                 time.sleep(0.5)
        #         # # # Starts servo at min position
        #         servo_position = -0.9
        #         servo.value = servo_position
        #     else:
        #         robot.value = movimento_anterior
        # else:
        #     contagem_verifica = contagem_verifica + 1

        
# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()

# try:
#     distance = 0
#     for i in range(0,10):
#         distancia = sensor_distance()
#         print(distancia)
#         distance = distance + distancia
#     print(distance/10)
# # If you press CTRL+C, cleanup and stop
# except KeyboardInterrupt:
#     exit()
