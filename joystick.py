import RPi.GPIO as GPIO
import spidev
import os
from time import sleep

MOTOR_EN_1_PIN = 14
MOTOR_A_1_PIN = 15
MOTOR_B_1_PIN = 18

MOTOR_EN_2_PIN = 23
MOTOR_A_2_PIN = 24
MOTOR_B_2_PIN = 25

LIGHT_PIN = 4

JOYSTICK_X_CHANNEL = 0
JOYSTICK_Y_CHANNEL = 1

DELAY = .1



def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def mixXY(x, y):
	"""
	mixes x and y from a joystick to values for a 2 motor drive system
	input: x (int or float), y (int or float)
	output: (leftMotor (float), rightMotor (float)) tuple
	"""
	leftMotor = y + x
	rightMotor = y - x

	return (leftMotor, rightMotor)

def setMotorPWMS(leftMotor, rightMotor):
    motors = mixXY(leftMotor, rightMotor)

    leftMotor = motors[0]
    rightMotor = motors[1]

    #left motor
    if leftMotor < -100:
        leftMotor = -100
    elif leftMotor > 100:
        leftMotor = 100
    if leftMotor == 0:
        motor1A.ChangeDutyCycle(0)
        motor1B.ChangeDutyCycle(0)
    elif leftMotor < 0:
        motor1A.ChangeDutyCycle(0)
        motor1B.ChangeDutyCycle(abs(leftMotor))
    else:
        motor1B.ChangeDutyCycle(0)
        motor1A.ChangeDutyCycle(leftMotor)

    #right motor
    if rightMotor < -100:
        rightMotor = -100
    elif rightMotor > 100:
        rightMotor = 100
    if rightMotor == 0:
        motor2A.ChangeDutyCycle(0)
        motor2B.ChangeDutyCycle(0)
    elif rightMotor < 0:
        motor2A.ChangeDutyCycle(0)
        motor2B.ChangeDutyCycle(abs(rightMotor))
    else:
        motor2B.ChangeDutyCycle(0)
        motor2A.ChangeDutyCycle(rightMotor)



#setup
spi = spidev.SpiDev()
spi.open(0,0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_EN_1_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_1_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_1_PIN, GPIO.OUT)

GPIO.setup(MOTOR_EN_2_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_2_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_2_PIN, GPIO.OUT)

GPIO.setup(LIGHT_PIN, GPIO.OUT)

motor1A = GPIO.PWM(MOTOR_A_1_PIN, 50)
motor1B = GPIO.PWM(MOTOR_B_1_PIN, 50)
motor2A = GPIO.PWM(MOTOR_A_2_PIN, 50)
motor2B = GPIO.PWM(MOTOR_B_2_PIN, 50)
motor1A.start(0)
motor1B.start(0)
motor2A.start(0)
motor2B.start(0)
GPIO.output(MOTOR_EN_1_PIN, 1)
GPIO.output(MOTOR_EN_2_PIN, 1)


light = True

try:
    while True:
        x = ReadChannel(JOYSTICK_X_CHANNEL)
        y = ReadChannel(JOYSTICK_Y_CHANNEL)
        x = (x - 500) / 5
        y = (y - 500) / 5
        setMotorPWMS(x,y)
        if light:
            GPIO.output(LIGHT_PIN, 1)
            light = False
        else:
            GPIO.output(LIGHT_PIN, 0)
            light = True
        sleep(DELAY)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("cleaned up")