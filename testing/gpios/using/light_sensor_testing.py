from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random


LDR_SLEEP_SEC = 1


# Is the UV light on? (self-check)
ledArray = ["UV off", "UV on"]
# Is the UV light on? (external-check)
ldrArray = ["UV off", "UV on"]

led = LED(6)
ldr0 = LightSensor(5)

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
uvSelfCheck, uvLDRCheck, uvBrightness = lightFunc()
print(f"Light self-check: {uvSelfCheck}, ldr external check: {uvLDRCheck}, ldr brightness: {uvBrightness} (0-1)")
