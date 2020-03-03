from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random

DHT_SLEEP_SEC = 1

# Is the machine overheating?
dhtTempArray = ["cool","hot"]
# Is there a humidity leak?
dhtHumiArray = ["dry", "humid"]

# Set sensor type : Options are DHT11, DHT22, or AM2302
dht0 = Adafruit_DHT.DHT22
dht0gpio = 13

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
internalHumid, internalTemp, humidity, temperatureC = dhtFunc()
print(f"Internal humidity: {internalHumid}, internal tempurature: {internalTemp}, humidity: {humidity}%, tempurature: {temperatureC}C")
