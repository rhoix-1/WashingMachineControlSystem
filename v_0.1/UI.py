# Platt Tech Nasa Hunch Team (Ethan Feldman & Josepher Shunaula)

# Imports
#import gpioDataCollector
#import mySQLConnector

# Ethan's Playground-------------------------------------------------------------
'''
import dataCollector
dataCollector.SendData()
'''


# Ethan's Playground-------------------------------------------------------------


import pygame

# Start UI
pygame.init()

# Results and Global Variables

# Resolutions
SCREEN_X = 800
SCREEN_Y = 480

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (66, 135, 245)


# Set screen size and title name
display = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
pygame.display.set_caption("Washing Machine")

display.fill(BLACK)

clock = pygame.time.Clock()
run = True

homePage = True

# Current Home Page button configuration
buttonTextOne = "Cycle Amounts"
buttonTextTwo = "Water Temp."
buttonTextThree = "Washing Duration"

def mainButtonOne(text):
	buttonFont = pygame.font.Font('Roboto/Roboto-Light.ttf', 25)
	buttonText = buttonFont.render(text, True, (WHITE))
	buttonTextLocation = buttonText.get_rect(midleft = (30, 30))
	pygame.draw.rect(display, WHITE, (30, 50, 40, 40))
	display.blit(buttonText, buttonTextLocation)

def mainButtonTwo(text):
	buttonFont = pygame.font.Font('Roboto/Roboto-Light.ttf', 25)
	buttonText = buttonFont.render(text, True, (WHITE))
	buttonTextLocation = buttonText.get_rect(midleft = (30, 120))
	pygame.draw.rect(display, WHITE, (30, 140, 40, 40))
	display.blit(buttonText, buttonTextLocation)

def mainButtonThree(text):
	buttonFont = pygame.font.Font('Roboto/Roboto-Light.ttf', 25)
	buttonText = buttonFont.render(text, True, (WHITE))
	buttonTextLocation = buttonText.get_rect(midleft = (30, 210))
	display.blit(buttonText, buttonTextLocation)
	pygame.draw.rect(display, WHITE, (30, 230, 40, 40))

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print("Exit Button Hit Closing UI")
			run = False

		# print(event)

	if homePage == True:
		mainButtonOne(buttonTextOne)
		mainButtonTwo(buttonTextTwo)
		mainButtonThree(buttonTextThree)

		'''
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					print("LEFT HIT")
				if event.key == pygame.K_RIGHT:
					print("RIGHT HIT")
		'''



	pygame.display.update()
	clock.tick(60)

pygame.quit()
quit()