# Platt Tech Nasa Hunch Team (Ethan Feldman & Josepher Shunaula)

import mysql.connector
import datetime
import random

#print("outside")

# Gets the current dataTime in the MySQL dateTime format
def Now():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# GPIO DATE COLLECTING ---------------------------------------------------------

def SelectedPreset():
	SPreset = ["Regular", "Whites", "Colors", "Permanent_Press", "Delicates", "Custom"]
	return SPreset[random.randint(0, 5)]

def AgitationSpeed():
	ASpeed = ["Fast", "Slow"]
	return ASpeed[random.randint(0, 1)]

def CycleSpeed():
	CSpeed = ["Fast", "Slow"]
	return CSpeed[random.randint(0, 1)]

def WaterTemperature():
	Temp = ["Warm", "Hot", "Cold"]
	return Temp[random.randint(0, 2)]

def Soak():
	Soak = ["No", "Yes"]
	return Soak[random.randint(0, 1)]

def ItemOfClothing():
	Item = ["Shirt", "Pants", "Underware", "Socks", "MiscSmall", "MiscMedium", "MiscLarge"]
	return Item[random.randint(0, 6)]

def AgitationWaterLevel():
	AWaterLevel = random.randint(200, 1000)
	return str(AWaterLevel) + "ml"

def AgitationWaterSalvaged():
	AWaterSalvaged = random.randint(200, 500)
	return str(AWaterSalvaged) + "ml"

def Lights():
	LightToggle = ["Off", "On"]
	L1 = LightToggle[random.randint(0,1)]
	L2 = LightToggle[random.randint(0,1)]
	L3 = LightToggle[random.randint(0,1)]
	return "L1: " + L1 + ", L2: " + L2 + ", L3: " + L3

def Motors():
	MotorToggle = ["Off", "On"]
	M1 = MotorToggle[random.randint(0,1)]
	M2 = MotorToggle[random.randint(0,1)]
	M3 = MotorToggle[random.randint(0,1)]
	return "M1: " + M1 + ", M2: " + M2 + ", M3: " + M3

def Valves():
	ValveToggle = ["Closed", "Open"]
	V1 = ValveToggle[random.randint(0,1)]
	V2 = ValveToggle[random.randint(0,1)]
	V3 = ValveToggle[random.randint(0,1)]
	return "V1: " + V1 + ", V2: " + V2 + ", V3: " + V3

def HumiditySensors():
	H1 = random.randint(0, 100)
	H2 = random.randint(0, 100)
	H3 = random.randint(0, 100)
	return "H1: " + str(H1) + "%, H2: " + str(H2) + "%, H3: " + str(H3) + "%"

def TemperatureSensors():
	T1 = random.randint(0, 100)
	T2 = random.randint(0, 100)
	T3 = random.randint(0, 100)
	return "T1: " + str(T1) + "F, T2: " + str(T2) + "F, T3: " + str(T3) + "F"

def PressureSensors():
	P1 = random.randint(0, 100)
	P2 = random.randint(0, 100)
	P3 = random.randint(0, 100)
	return "P1: " + str(P1) + "psi, P2: " + str(P2) + "psi, P3: " + str(P3) + "psi"


# MYSQL DATA SENDING -----------------------------------------------------------
def SendData():

	#print("inside")

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
	sql = "INSERT INTO logs (SelectedPreset, AgitationSpeed, CycleSpeed, WaterTemperature, Soak, ItemOfClothing, AgitationWaterLevel, AgitationWaterSalvaged, Lights, Valves, Motors, HumiditySensors, TemperatureSensors, PressureSensors, DateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	logSPreset = SelectedPreset()
	logASpeed = AgitationSpeed()
	logCSpeed = CycleSpeed()
	logTemp = WaterTemperature()
	logSoak = Soak()
	logItem = ItemOfClothing()
	logAWaterLevel = AgitationWaterLevel()
	logAWaterSalvaged = AgitationWaterSalvaged()
	logLights = Lights()
	logValves = Valves()
	logMotors = Motors()
	logHSensors = HumiditySensors()
	logTSensors = TemperatureSensors()
	logPSensors = PressureSensors()
	val = (logSPreset, logASpeed, logCSpeed, logTemp, logSoak, logItem, logAWaterLevel, logAWaterSalvaged, logLights, logValves, logMotors, logHSensors, logTSensors, logPSensors, Now())
	print(sql, val)
	mycursor.execute(sql, val)

	mydb.commit()
