from gpiozero import LED, LightSensor, Button, DistanceSensor, PWMOutputDevice, AngularServo
from signal import pause
from gpiozero import PWMLED
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import random

blue = LED(6)
blue.blink()
pause()
