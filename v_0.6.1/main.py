# Platt Tech Nasa Hunch Team (Ethan Feldman & Josepher Shunaula)
import kivy
import time
import random
import datetime
import mysql.connector
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


# GPIO DATE COLLECTING
itemOfClothing = ["Shirt", "Pants", "Sock", "Underwear", "Towel", "Custom"]
aSpeed = ["Fast", "Slow"]
cSpeed = ["Fast", "Slow"]
soakItem = ["No", "Yes"]
waterAmount = ["Small", "Medium", "Large"]
# ------------------------------------------------------------------------------
LightToggle = ["Off", "On"]
MotorToggle = ["Off", "On"]
PumpToggle = ["Off", "On"]
ValveToggle = ["Closed", "Open"]

# KEEPS TRACK OF YOUR SELECTION TO ALLOW YOU TO SEE THE CHOICES
selectionCounter = 0



# Now
#   CURRENT TIME AND DATE
def Now():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ALL THESE FUNCTION ARE A PLACEHOLDER FOR THE REAL INFORMATION -------------------------
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
# --------------------------------------------------------------------------------------------

# sendData
#   SENDS DATA TO MYSQL DATABASE
def sendData():

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
	sql = "INSERT INTO settings (DateTime, ItemOfClothing, AgitationSpeed, CycleSpeed, Soak, WaterAmount) VALUES (%s, %s, %s, %s, %s, %s)"
	val = (Now(), setItemOfClothing, setASpeed, setCSpeed, setSoak, setWaterAmount)
	print(sql, val)
	mycursor.execute(sql, val)

	mydb.commit()

class HomeWindow(Screen):
	'''
	def __init__(self, **kwargs):
		super(HomeWindow, self).__init__(**kwargs)
		Clock.schedule_interval(self.SetDateTime, 1)
	'''

	# clothingSelection
	# 	FILLS IN CLOTHING PRESET SELECTION
	def clothingSelection(self):
		print("HEY THERE WE ARE TESTING")
		'''
		if clothingID.text == "Shirt":
			print("Shirts are here")
		'''

	# userInputSelections
	#   ALLOWS YOU TO SELECT THROUGH YOUR CHOICES
	def userInputSelections(self, currentSelection, totalSelection, currentButton):
		global selectionCounter
		totalSelection = eval(totalSelection)
		if selectionCounter < len(totalSelection):
			currentSelection.text = str(totalSelection[selectionCounter])
			if currentButton == "clothingID":
				HomeWindow().clothingSelection()
			selectionCounter += 1
		else:
			selectionCounter = 0
			currentSelection.text = str(totalSelection[selectionCounter])
			selectionCounter += 1

	# doneButton
	# SAVES ALL INFORMATION THAT IS SELECTED
	def doneButton(self, presetsID, agitationSpeedID, cycleSpeedID, soakItemID, waterAmountID):
		global setItemOfClothing
		global setASpeed
		global setCSpeed
		global setSoak
		global setWaterAmount
		setItemOfClothing = presetsID.text
		setASpeed = agitationSpeedID.text
		setCSpeed = cycleSpeedID.text
		setSoak = soakItemID.text
		setWaterAmount = waterAmountID.text
		sendData()



	def SetDateTime(self, *args):
		print(HomeWindow().ids.dateTimeID.text)
		HomeWindow().ids.dateTimeID.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	'''
	def SetDateTime(dt):
		# print(HomeWindow().ids.dateTimeID.text)

		text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print(text)
		return text

		# dateTimeID.text = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		# HomeWindow().ids.dateTimeID.text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	# Clock.schedule_interval(SetDateTime, 1)
	'''

class SettingsWindow(Screen):
	pass


class WindowManager(ScreenManager):
	pass


class WashingMachineUI(App):
	def build(self):
		return


if __name__ == "__main__":
	WashingMachineUI().run()
