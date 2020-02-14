from gpiozero import Button, LED
import RPi.GPIO as GPIO
from time import sleep

# Variables
BUTTON_BOUNCE_SLEEP_SEC = 0.15

# Hardware GPIO setup
btn0 = Button(17)
btn1 = Button(27)
btn2 = Button(22)
btn3 = Button(9)
btn4 = Button(11)
btn5 = Button(5)
btn6 = Button(6)
btn7 = Button(13)
btn8 = Button(19)
btn9 = Button(26)
led = LED(25)

# Data collection
while True:
	if btn0.is_pressed:
		led.off()
		print("Off")
	elif btn1.is_pressed:
		print("Btn 1")
	elif btn2.is_pressed:
		print("Btn 2")
	elif btn3.is_pressed:
		print("Btn 3")
	elif btn4.is_pressed:
		print("Btn 4")
	elif btn5.is_pressed:
		print("Btn 5")
	elif btn6.is_pressed:
		print("Btn 6")
	elif btn7.is_pressed:
		print("Btn 7")
	elif btn8.is_pressed:
		print("Btn 8")
	elif btn9.is_pressed:
		led.on()
		print("On")
	#else:
	
	sleep(BUTTON_BOUNCE_SLEEP_SEC)
		

# Just in case, cleanup GPIO signals
GPIO.cleanup()
