import RPi.GPIO as GPIO
import spidev
import os
from time import sleep
from os import stat

MOTOR_EN_1_PIN = 14
MOTOR_A_1_PIN = 15
MOTOR_B_1_PIN = 18

MOTOR_EN_2_PIN = 23
MOTOR_A_2_PIN = 24
MOTOR_B_2_PIN = 25

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
    print("left Motor: ", leftMotor)
    if leftMotor == 0:
        GPIO.output(MOTOR_EN_1_PIN, 0)
        motor1A.stop()
        motor1B.stop()
    elif leftMotor < 0:
        GPIO.output(MOTOR_EN_1_PIN, 1)
        motor1A.stop()
        motor1B.ChangeDutyCycle(abs(leftMotor))
    else:
        GPIO.output(MOTOR_EN_1_PIN, 1)
        motor1A.ChangeDutyCycle(leftMotor)
        motor1B.stop()

    #right motor
    if rightMotor < -100:
        rightMotor = -100
    elif rightMotor > 100:
        rightMotor = 100
    print("right motor: ", rightMotor)
    if rightMotor == 0:
        GPIO.output(MOTOR_EN_2_PIN, 0)
        motor2A.stop()
        motor2B.stop()
    elif rightMotor < 0:
        GPIO.output(MOTOR_EN_2_PIN, 1)
        motor2A.stop()
        motor2B.ChangeDutyCycle(abs(rightMotor))
    else:
        GPIO.output(MOTOR_EN_2_PIN, 1)
        motor2A.ChangeDutyCycle(rightMotor)
        motor2B.stop()



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

motor1A = GPIO.PWM(MOTOR_A_1_PIN, 50)
motor1B = GPIO.PWM(MOTOR_B_1_PIN, 50)
motor2A = GPIO.PWM(MOTOR_A_2_PIN, 50)
motor2B = GPIO.PWM(MOTOR_B_2_PIN, 50)
motor1A.start(0)
motor1B.start(0)
motor2A.start(0)
motor2B.start(0)



while True:
    pass

try:
    while True:
        x = ReadChannel(JOYSTICK_X_CHANNEL)
        y = ReadChannel(JOYSTICK_Y_CHANNEL)
        setMotorPWMS(x,y)
except KeyboardInterrupt:
    GPIO.cleanup()