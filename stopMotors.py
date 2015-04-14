import RPi.GPIO as GPIO
from time import sleep

MOTOR_EN_1_PIN = 14
MOTOR_A_1_PIN = 15
MOTOR_B_1_PIN = 18

MOTOR_EN_2_PIN = 23
MOTOR_A_2_PIN = 24
MOTOR_B_2_PIN = 25


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



GPIO.setwarnings(False)

#setup
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


GPIO.output(MOTOR_EN_1_PIN,0)
GPIO.output(MOTOR_EN_2_PIN,0)
motor1A.ChangeDutyCycle(0)
motor1B.ChangeDutyCycle(0)
motor2A.ChangeDutyCycle(0)
motor2B.ChangeDutyCycle(0)

sleep(1)