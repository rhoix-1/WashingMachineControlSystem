# Platt Tech Nasa Hunch Team (Ethan Feldman & Josepher Shunaula)

import mysql.connector
import datetime
import random

#print("outside")

# Gets the current dataTime in the MySQL dateTime format
def Now():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# GPIO DATE COLLECTING ---------------------------------------------------------
SPreset = ["Color", "White", "Pants", "Socks", "Underwear", "Towels", "Custom"]
ASpeed = ["Fast", "Slow"]
CSpeed = ["Fast", "Slow"]
soakItem = ["No", "Yes"]
# ------------------------------------------------------------------------------
Item = ["Shirt", "Pants", "Underware", "Socks", "MiscSmall", "MiscMedium", "MiscLarge"]
LightToggle = ["Off", "On"]
MotorToggle = ["Off", "On"]
PumpToggle = ["Off", "On"]
ValveToggle = ["Closed", "Open"]

def SelectedPreset():
	return SPreset[random.randint(0, 6)]

def AgitationSpeed():
	return ASpeed[random.randint(0, 1)]

def CycleSpeed():
	return CSpeed[random.randint(0, 1)]

def Soak():
	return soakItem[random.randint(0, 1)]

def ItemOfClothing():
	return Item[random.randint(0, 6)]

def AgitationWaterLevel():
	AWaterLevel = random.randint(200, 1000)
	return str(AWaterLevel) + "ml"

def AgitationWaterSalvaged():
	AWaterSalvaged = random.randint(200, 500)
	return str(AWaterSalvaged) + "ml"

def Lights():
	L1 = LightToggle[random.randint(0,1)]
	L2 = LightToggle[random.randint(0,1)]
	L3 = LightToggle[random.randint(0,1)]
	return "L1: " + L1 + ", L2: " + L2 + ", L3: " + L3

def Motors():
	M1 = MotorToggle[random.randint(0,1)]
	M2 = MotorToggle[random.randint(0,1)]
	M3 = MotorToggle[random.randint(0,1)]
	return "M1: " + M1 + ", M2: " + M2 + ", M3: " + M3

def Pumps():
	P1 = PumpToggle[random.randint(0,1)]
	P2 = PumpToggle[random.randint(0,1)]
	P3 = PumpToggle[random.randint(0,1)]
	return "P1: " + P1 + ", P2: " + P2 + ", P3: " + P3

def Valves():
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

	mydb = mysql.connector.connect(
	)

	# This will execute commands
	mycursor = mydb.cursor()

	# sql commands
	# val passes data in %s, %s
	
	# --- LOGS ---
	sql = "INSERT INTO logs (DateTime, AgitationWaterLevel, AgitationWaterSalvaged, Lights, Valves, Motors, Pumps, HumiditySensors, TemperatureSensors, PressureSensors) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	logAWaterLevel = AgitationWaterLevel()
	logAWaterSalvaged = AgitationWaterSalvaged()
	logLights = Lights()
	logValves = Valves()
	logMotors = Motors()
	logPumps = Pumps()
	logHSensors = HumiditySensors()
	logTSensors = TemperatureSensors()
	logPSensors = PressureSensors()
	val = (Now(), logAWaterLevel, logAWaterSalvaged, logLights, logValves, logMotors, logPumps, logHSensors, logTSensors, logPSensors)
	print(sql, val)
	mycursor.execute(sql, val)

	mydb.commit()
	
	# --- SETINGS ---
	sql = "INSERT INTO settings (DateTime, SelectedPreset, AgitationSpeed, CycleSpeed, Soak) VALUES (%s, %s, %s, %s, %s)"
	setSPreset = SelectedPreset()
	setASpeed = AgitationSpeed()
	setCSpeed = CycleSpeed()
	setSoak = Soak()
	val = (Now(), setSPreset, setASpeed, setCSpeed, setSoak)
	print(sql, val)
	mycursor.execute(sql, val)

	mydb.commit()
