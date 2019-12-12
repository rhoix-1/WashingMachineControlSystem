from gpiozero import Button, LED
from time import sleep

n = 0
btn0 = Button(2)
btn1 = Button(3)
btn2 = Button(17)
btn3 = Button(27)
btn4 = Button(13)
btn5 = Button(19)
btn6 = Button(26)
btn7 = Button(16)
btn8 = Button(20)
btn9 = Button(21)

led0 = LED(18)

while True:
	if btn0.is_pressed:
		n = 0
		led0.off()
		print(n)
	elif btn1.is_pressed:
		n = n + 1
		print(n)
	elif btn2.is_pressed:
		n = n + 2
		print(n)
	elif btn3.is_pressed:
		n = n + 3
		print(n)
	elif btn4.is_pressed:
		n = n + 4
		print(n)
	elif btn5.is_pressed:
		n = n + 5
		print(n)
	elif btn6.is_pressed:
		n = n + 6
		print(n)
	elif btn7.is_pressed:
		n = n + 7
		print(n)
	elif btn8.is_pressed:
		n = n + 8
		print(n)
	elif btn9.is_pressed:
		n = n + 9
		led0.on()
		print(n)
	#else:
	
	sleep(0.1)
		
