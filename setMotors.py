import RPi.GPIO as GPIO
from sys import argv

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
    if leftMotor < 0:
        GPIO.output(MOTOR_B_1_PIN, 1)
        GPIO.output(MOTOR_A_1_PIN, 0)
        motor1PWM.ChangeDutyCycle(leftMotor)
    else:
        GPIO.output(MOTOR_A_1_PIN, 1)
        GPIO.output(MOTOR_B_1_PIN, 0)
        motor1PWM.ChangeDutyCycle(leftMotor)

    #right motor
    if rightMotor < 0:
        GPIO.output(MOTOR_B_2_PIN, 1)
        GPIO.output(MOTOR_A_2_PIN, 0)
        motor2PWM.ChangeDutyCycle(leftMotor)
    else:
        GPIO.output(MOTOR_A_2_PIN, 1)
        GPIO.output(MOTOR_B_2_PIN, 0)
        motor2PWM.ChangeDutyCycle(leftMotor)


GPIO.setwarnings(False)

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_EN_1_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_1_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_1_PIN, GPIO.OUT)

GPIO.setup(MOTOR_EN_2_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_2_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_2_PIN, GPIO.OUT)

motor1PWM = GPIO.PWM(MOTOR_EN_1_PIN, 50)
motor2PWM = GPIO.PWM(MOTOR_EN_2_PIN, 50)
motor1PWM.start(0)
motor2PWM.start(0)


if len(argv) <= 2:
    print("Need to call with x and y from commandline")
else:
    if argv[1].isdigit() and argv[2].isdigit():
        motorPWM = mixXY(int(argv[1]), int(argv[2]))
        leftMotorPWM = motorPWM[0]
        rightMotorPWM = motorPWM[1]
        print("left motor:",leftMotorPWM)
        print("right motor:", rightMotorPWM)
        setMotorPWMS(leftMotorPWM, rightMotorPWM)
    else:
        print("Need to call with x and y as integers")