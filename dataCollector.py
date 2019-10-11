# Platt Tech Nasa Hunch Team (Ethan Feldman & Josepher Shunaula)

import mysql.connector
import datetime
import random

#print("outside")

# Gets the current dataTime in the MySQL dateTime format
def Now():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# GPIO DATE COLLECTING ---------------------------------------------------------

# Toggle the light as OFF or ON
def lightToggle():
	toggle = ['OFF', 'ON']
	return 'The Light is ' + toggle[random.randint(0, 1)]

# The water level in PINTS
def waterLevel():
	return 'Water Level is at ' + str(random.randint(0, 10)) + ' PINTS'


# MYSQL DATA SENDING -----------------------------------------------------------
def SendData():

	#print("inside")

	lightToggleValue = lightToggle()
	waterLevelValue = waterLevel()

	# Connects to justin's MySQL server on his computer
	# His IP-Addess: 24.2.213.138
	mydb = mysql.connector.connect(
		host="mysql.kellyweb.space",
		user="roboto",
		passwd="@Plattist1",
		database="hunch"
	)

	# This will execute commands
	mycursor = mydb.cursor()

	# sql commands
	# val passes data in %s, %s
	sql = "INSERT INTO logs (info, dateTime) VALUES (%s, %s)"
	log = lightToggleValue + ', ' + waterLevelValue
	val = (log, Now())
	print(sql, val)
	mycursor.execute(sql, val)

	mydb.commit()
