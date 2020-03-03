from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random

MOTOR_RPM = 182

# Is the motor active and what dirrection?
motArray = ["Stopped", "Forward", "Reverse"]

# Set forward and backward motor drives
IN1 = 17 # - Forwards
IN2 = 27 # - Backwards
forwardDrive = PWMOutputDevice(IN1, True, 0, 1000)
backwardDrive = PWMOutputDevice(IN2, True, 0, 1000)

# Motor Functions
def Stop():
	forwardDrive.value = 0
	backwardDrive.value = 0
	
def Forward(s):
	forwardDrive.value = s
	backwardDrive.value = 0

def Backward(s):
	forwardDrive.value = 0
	backwardDrive.value = s

# Motor data collection
# Takes dirrect, speed (rpm), and duration
# Returns motorDirection, motorSpeed, motorDuration
def motorFunc(direction, speed, duration):
	
	# gpiozero uses a 0-1 scale, so I have to divid rpm values by MOTOR_RPM
	s = round(speed / MOTOR_RPM, 3)
	
	# Lets you select which way the motor drives
	if direction == 1:
		Forward(s)
		sleep(duration)
		Stop()
	elif direction == -1:
		Backward(s)
		sleep(duration)
		Stop()
	elif direction == 0: 
		Stop()
		sleep(MOTOR_SLEEP_SEC)
		Stop()
	
	return motArray[direction], speed, duration

# How to use motorFunc()
motorDirection, agitationMotorSpeedRPM, motorDuration = motorFunc(1, 60, 5)
print(f"Motor state: {motorDirection}, motor speed: {agitationMotorSpeedRPM} rpm (base=200rpm), duration {motorDuration} sec")

motorDirection, cycleMotorSpeedRPM, motorDuration = motorFunc(-1, 60, 5)
print(f"Motor state: {motorDirection}, motor speed: {cycleMotorSpeedRPM} rpm (base=200rpm), duration {motorDuration} sec")

