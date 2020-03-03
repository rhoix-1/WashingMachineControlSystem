from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random

DIS_SLEEP_SEC = 1

# Is there an item in the machine?
disArray = ["intake empty", "intake loaded"]

dis0 = DistanceSensor(echo=26, trigger=19)

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
		i = 1
	else:	
		i = 0
	
	return i, d

# How to use distanceFunc()
# str, int (cm)
print("1 hi")
itemIntakeLoaded, itemDistance = distanceFunc()
print("2 hi")
print(f"Item check: {itemIntakeLoaded}, item distance: {itemDistance}")
print("3 hi")
itemDispenseUnloaded, itemDistance = distanceFunc()
print("4 hi")
print(f"Item check: {itemDispenseUnloaded}, item distance: {itemDistance}")
print("5 hi")
