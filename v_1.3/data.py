# Platt Tech NASA HUNCH Team
# Ethan R Feldman
# Josepher Shunaula

from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random


# Variables ------------------------------------------------------------

# Sleeps in seconds
BTN_BOUNCE_SLEEP_SEC = 0.15
LDR_SLEEP_SEC = 1
DIS_SLEEP_SEC = 1
DHT_SLEEP_SEC = 1
SERVO_SLEEP_SEC = 0.5
MOTOR_RPM = 182


# Is the UV light on? (self-check)
ledArray = ["UV off", "UV on"]
# Is the UV light on? (external-check)
ldrArray = ["UV off", "UV on"]
# What button was pressed?
btnArray = ["Button 0", "Button 1", "Button 2", "Button 3", "Button 4", "Button 5", "Button 6", "Button 7", "Button 8", "Button 9"]
# Is there an item in the machine?
disArray = ["intake empty", "intake loaded"]
# Is the valve open?
serArray = ["valve closed", "valve open", "valve blocked"]
# Is the machine overheating?
dhtTempArray = ["cool","hot"]
# Is there a humidity leak?
dhtHumiArray = ["dry", "humid"]
# Is the motor active and what dirrection?
motArray = ["Stopped", "Forward", "Reverse"]

# Raw values
# l = lightSelfCheck
# e = lightExternalCheck
# b = brightness
# i = itemCheck
# d = distance
# v = valve opened/closed
# a = servo angle
# t = tempurature
# h = humidity
# direction = motor stop/forward/reverse
# s = motor speed
# duration = motor sleep duration

# Hardware -------------------------------------------------------------

# GPIO
led = LED(26)
ldr0 = LightSensor(16)
btn0 = Button(25)
btn1 = Button(17)
btn2 = Button(27)
btn3 = Button(22)
btn4 = Button(9)
btn5 = Button(11)
btn6 = Button(5)
btn7 = Button(6)
btn8 = Button(13)
btn9 = Button(19)
dis0 = DistanceSensor(echo=23, trigger=24)
servo0 = AngularServo(18, initial_angle=0, min_angle=0, max_angle=90)

# Set sensor type : Options are DHT11, DHT22, or AM2302
dht0 = Adafruit_DHT.DHT22
dht0gpio = 12

# Set forward and backward motor drives
IN1 = 21 # - Forwards
IN2 = 20 # - Backwards
forwardDrive = PWMOutputDevice(IN1, True, 0, 1000)
backwardDrive = PWMOutputDevice(IN2, True, 0, 1000)


# Functions ------------------------------------------------------------

# Item distance collection
# Returns itemCheck, itemDistance
def distanceFunc():
	
	sleep(DIS_SLEEP_SEC)
	
	# Gets data: distance in meters
	# Converts in centimeters
	# Rounds to 3 decimal places
	d = round(dis0.distance * 100, 3)
	
	# Checks distance id bellow 10 cm
	if d < 10.0:
		i = True
	else:	
		i = False
	
	return i, d

# How to use distanceFunc()
# str, int (cm)
#itemIntakeLoaded, itemDistance = distanceFunc()
#print(f"Item check: {itemIntakeLoaded}, item distance: {itemDistance}")


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
		v = False
		a = 0
	elif servo0.angle == 90:
		# Valve opened
		v = True
		a = 90
	
	return v, a

# How to use servoFunc()
#waterValeOpened, servoAngle = servoFunc()
#print(f"Valve state: {waterValeOpened}, servo angle: {servoAngle}")


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
#motorDirection, agitationMotorSpeedRPM, motorDuration = motorFunc(1, 60, 5)
#print(f"Motor state: {motorDirection}, motor speed: {agitationMotorSpeedRPM} rpm (base=200rpm), duration {motorDuration} sec")

#motorDirection, cycleMotorSpeedRPM, motorDuration = motorFunc(-1, 10, 5)
#print(f"Motor state: {motorDirection}, motor speed: {cycleMotorSpeedRPM} rpm (base=200rpm), duration {motorDuration} sec")


# Humidity and Temperature collection
# Returns internalTemp, internalHumid, tempValue, humidValue
def dhtFunc():
	
	# Use read_retry method. This will retry up to 15 times to
	# get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(dht0, dht0gpio)
	
	# Reading the DHT11 is very sensitive to timings and occasionally
	# the Pi might fail to get a valid reading. So check if readings are valid.
	while humidity is None and temperature is None:
		humidity, temperature = Adafruit_DHT.read_retry(dht0, dht0gpio)
	
	# Rounds values
	h = round(humidity, 1)
	t = round(temperature, 1)
	
	# Checks if humidity is above 50%
	if h > 50.0:
		hBool = 1
	else:
		hBool = 0
	
	# Checks if tempuratue is above 20C
	if t > 20.0:
		tBool = 1
	else:
		tBool = 0
	
	return dhtHumiArray[hBool], dhtTempArray[tBool], h, t

# How to use dhtFunc()
#internalHumid, internalTemp, humidity, temperatureC = dhtFunc()
#print(f"Internal humidity: {internalHumid}, internal tempurature: {internalTemp}, humidity: {humidity}%, tempurature: {temperatureC}C")


# UV light collection
# Returns lightSelfCheck, lightExternalCheck, brightness
def lightFunc():
	
	sleep(LDR_SLEEP_SEC)
	
	# Turns on light
	led.on()
	
	# light = 1 (True)
	l = 1
	
	sleep(LDR_SLEEP_SEC)
	
	# Gets data: brightness value 	
	# Rounds to 3 decimal places
	b = round(ldr0.value, 3)
	
	# Checks brightness value if above 0.8
	if b > 0.8:
		e = 1
	else:
		e = 0
	
	# Turns off light
	led.off()
	
	return l, e, b

# How to use lightFunc()
#uvSelfCheck, uvLDRCheck, uvBrightness = lightFunc()
#print(f"Light self-check: {uvSelfCheck}, ldr external check: {uvLDRCheck}, ldr brightness: {uvBrightness} (0-1)")


