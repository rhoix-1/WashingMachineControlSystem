from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random

SERVO_SLEEP_SEC = 0.5

# Is the valve open?
serArray = ["valve closed", "valve open", "valve blocked"]

servo0 = AngularServo(22, initial_angle=0, min_angle=0, max_angle=90)

# Servo data collection
# Returns valveSate, servoAngle, servoCounter
def servoFunc():
	
	# Resets servo
	servo0.angle = 0
	
	sleep(SERVO_SLEEP_SEC)
	
	# servo 90
	servo0.angle = 90
	
	sleep(SERVO_SLEEP_SEC)
	
	if servo0.angle == 0:
		# Valve closed
		v = 0
		a = 0
	elif servo0.angle == 90:
		# Valve opened
		v = 1
		a = 90
	
	return v, a

# How to use servoFunc()
waterValveOpened, servoAngle = servoFunc()
print(f"Valve state: {waterValveOpened}, servo angle: {servoAngle}")
