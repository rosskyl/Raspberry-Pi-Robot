import RPi.GPIO as GPIO
import time

#constants
MOTOR_EN_1_PIN = 14
MOTOR_A_1_PIN = 15
MOTOR_B_1_PIN = 18

MOTOR_EN_2_PIN = 23
MOTOR_A_2_PIN = 24
MOTOR_B_2_PIN = 25

WAIT = 2
SMALL_WAIT = .02



def motorsFull():
	#enable motors
	GPIO.output(MOTOR_EN_1_PIN, 1)
	GPIO.output(MOTOR_EN_2_PIN, 1)

	#enable motors control pin a
	GPIO.output(MOTOR_A_1_PIN,1)
	GPIO.output(MOTOR_A_2_PIN,1)

	time.sleep(WAIT)

	#disable motors control pin a
	GPIO.output(MOTOR_A_1_PIN,0)
	GPIO.output(MOTOR_A_2_PIN,0)

	time.sleep(WAIT)

	#enable motors control pin b
	GPIO.output(MOTOR_B_1_PIN,1)
	GPIO.output(MOTOR_B_2_PIN,1)

	time.sleep(WAIT)

	#disable motors control pin b
	GPIO.output(MOTOR_B_1_PIN,0)
	GPIO.output(MOTOR_B_2_PIN,0)

def motorsPWM():
	#enable motors
	GPIO.output(MOTOR_EN_1_PIN, 1)
	GPIO.output(MOTOR_EN_2_PIN, 1)
	
	#setup PWM for control pins
	motor1A = GPIO.PWM(MOTOR_A_1_PIN, 50)
	motor1B = GPIO.PWM(MOTOR_B_1_PIN, 50)
	motor2A = GPIO.PWM(MOTOR_A_2_PIN, 50)
	motor2B = GPIO.PWM(MOTOR_B_2_PIN, 50)
	motor1A.start(0)
	motor1B.start(0)
	motor2A.start(0)
	motor2B.start(0)
	
	#both motors rev up
	for i in range(0,100):
		motor1A.ChangeDutyCycle(i)
		motor2A.ChangeDutyCycle(i)
		time.sleep(SMALL_WAIT)
		
	time.sleep(WAIT)
		
	#rev motors down
	for i in range(100,0,-1):
		motor1A.ChangeDutyCycle(i)
		motor2A.ChangeDutyCycle(i)
		time.sleep(SMALL_WAIT)
		
def mixXY(x, y):
	"""
	mixes x and y from a joystick to values for a 2 motor drive system
	input: x (int or float), y (int or float)
	output: (leftMotor (float), rightMotor (float)) tuple
	"""
	leftMotor = y + x
	rightMotor = y - x
	
	return (leftMotor, rightMotor)
	

	



#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_EN_1_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_1_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_1_PIN, GPIO.OUT)

GPIO.setup(MOTOR_EN_2_PIN, GPIO.OUT)
GPIO.setup(MOTOR_A_2_PIN, GPIO.OUT)
GPIO.setup(MOTOR_B_2_PIN, GPIO.OUT)


motorsFull()
#motorsPWM()



GPIO.cleanup()
