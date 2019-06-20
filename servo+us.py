from gpiozero import Servo
from time import sleep
import time
from gpiozero import DistanceSensor

#Pino servo GPIO19 (35)
#Pino US Echo GPIO 16 (36)
#Pino US Trig GPIO 13 (33)

pinServo = 19
pinEcho = 16
pinTrig = 13

myCorrection=0.45
maxPW=(2.0+myCorrection+0.01)/1000
minPW=(1.0-myCorrection)/1000

servo = Servo(pinServo,min_pulse_width=minPW,max_pulse_width=maxPW)
sensor = DistanceSensor(echo=pinEcho, trigger=pinTrig)

#Starts servo at min position
servo_position = 1.0
servo.value = servo_position

###############################################################################
#Teste Servo 

# while True:
#     servo.value = 0
#     print("mid")
#     sleep(0.5)
#     servo.value = -1
#     print("min")
#     sleep(1)
#     servo.value = 0
#     print("mid")
#     sleep(0.5)
#     servo.value = 1
#     print("max")
#     sleep(1)

################################################################################
#Teste US

# try:
#     while True:
#         print('Distance: ', sensor.distance * 100)

################################################################################

try:
    while True:
        #comeca com servo olhando para frente
        if (sensor.distance*100) > 20:
            print('segue linha')
        else:
            print('robot.stop()')
            sleep(1)
            print('robot left 90 while servo seek')
            sleep(1)
            starttime = time.time()
            while (time.time() - starttime) < 60:#while not iscenterblack:
                if (sensor.distance*100) > 20:
                	print('robot.stop()')
                	starttime2 = time.time()
                	direction = -0.05
                	while ((sensor.distance*100) > 20) and ((time.time() - starttime2) < 5.0):
						print('servo seek')
						if (servo_position < -0.95 and direction == -0.05) or (servo_position > 0.95 and direction == 0.05):
							direction = -direction
						servo_position += direction
						print(servo_position)
						servo.value = servo_position
						sleep(0.03)
                elif (sensor.distance*100) < 10:
                    print('robot left')
                elif (sensor.distance*100) > 15:
                    print('robot right')
                else:
                	print('robot forward')

# If you press CTRL+C, cleanup and stop
except KeyboardInterrupt:
    exit()