import sys
import Adafruit_DHT

sensor = 11
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
temperature = temperature * 9/5.0 + 32

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}'.format(temperature))
else:
    print('Failed to get temp. Try again.')
sys.exit(1)