# Platt Tech NASA HUNCH Team
# Josepher E. Shunaula
# Ethan R. Feldman

import time
import threading
from data import *
import tkinter as tk
import mysql.connector
from tkinter import ttk
from gpiozero import Button
from datetime import datetime

# Preset Variables ---
dataTimeStartPreset = -1
itemSelection = "Custom"
sizeSelection = "Large"
agitationSelection = "Fast"
cycleSelection = "Slow"
soakSelection = "Yes"
agitationSpeedRPM = 110
agitationDurationMIN = 10
cycleSpeedRPM = 60
cycleDurationMIN = 2
waterAmountML = 1000
soakDurationMIN = 10

# Log Varibles---
dateTimeStartIntake = -1
itemIntakeLoaded = -1
dateTimeStartAgitation = -1 
waterValveOpened = -1
#waterAmountML
waterLoaded = -1
agitationMotorSpeedRPM = -1
dateTimeStartSoak = -1
waterSalvagedML = -1
dateTimeStartCycle = -1
cycleMotorSpeedRPM = -1
humidityValue = -1
temperatureValueC = -1
dateTimeStartUVLight = -1
uvSelfCheckActive = -1
uvLDRCheckActive = -1
uvBrightness = -1
dateTimeStartDispense = -1
itemDispenseUnloaded = -1


'''

mydb = mysql.connector.connect(
)

# This will execute commands
mycursor = mydb.cursor()
'''

# Gets the current dataTime in the MySQL dateTime format
def Now():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sendRawPresetData():
	# Appending to raw Preset.txt
	linePreset = f"({dataTimeStartPreset}, {itemSelection}, {sizeSelection}, {agitationSelection}, {cycleSelection}, {soakSelection}, {agitationSpeedRPM}, {agitationDurationMIN}, {cycleSpeedRPM}, {cycleDurationMIN}, {waterAmountML}, {soakDurationMIN})"
	print(linePreset)
	filePreset = open("rawPreset.txt", "a")
	filePreset.write(linePreset)
	filePreset.write("\n")
	filePreset.close()
	
	'''
	# Sending to Preset table
	sqlPreset = "INSERT INTO preset (dateTime, item, size, agitation, cycle, soak, agitationSpeedRPM, agitationDurationMIN, cycleSpeedRPM, cycleDurationMIN, waterAmountML, soakDurationMIN) VALUES " + linePreset
	print(sqlPreset)
	mycursor.execute(sqlPreset)
	mydb.commit()
	'''
	
def sendRawLogData():
	# Appending to rawLog.txt
	lineLog = f"({dateTimeStartIntake}, {itemIntakeLoaded}, {dateTimeStartAgitation}, {waterValveOpened}, {waterAmountML}, {waterLoaded}, {agitationMotorSpeedRPM}, {dateTimeStartSoak}, {waterSalvagedML}, {dateTimeStartCycle}, {cycleMotorSpeedRPM}, {humidityValue}, {temperatureValueC}, {dateTimeStartUVLight}, {uvSelfCheckActive}, {uvLDRCheckActive}, {uvBrightness}, {dateTimeStartDispense}, {itemDispenseUnloaded})"
	print(lineLog)
	fileLog = open("rawLog.txt", "a")
	fileLog.write(lineLog)
	fileLog.write("\n")
	fileLog.close()
	
	'''
	# Sending to Log table
	sqlLog = "INSERT INTO log (dateTimeStartIntake, itemIntakeLoaded, dateTimeStartAgitation, waterValveOpened, waterLevelML, waterLoaded, agitationMotorSpeedRPM, dateTimeStartSoak, waterSalvagedML, dateTimeStartCycle, cycleMotorSpeedRPM, humidity, temperatureC, dateTimeStartUVLight, uvSelfCheckActive, uvLDRCheckActive, uvBrightness, dateTimeStartDispense, itemDispenseUnloaded) VALUES " + lineLog
	print(sqlLog)
	mycursor.execute(sqlLog)
	mydb.commit()
	'''
# ----------------------------------------------------------------------

# Home Window
# Text/Button Design
TEXT_FONT = ("Roboto", 20)
TEXT_COLOR = "white"
TEXT_BACKGROUND_COLOR = "black"
BUTTON_FONT = ("Roboto", 15)

SMALLER_FONT = ("Roboto", 15)
SMALLER_BUTTON_FONT = ("Roboto", 12)

# Preset_Builder
#   It builds an object containing the preset and its information
class Preset_Builder:
	def __init__(self, item, size, agitation, cycle, soak):
		self.item = item
		self.size = size
		self.agitation = agitation
		self.cycle = cycle
		self.soak = soak

# Where all the preset objects are
presets_list = []

# Creates an object using the Preset_Builder class
# It then appends it to the presets_list to store it all in one place
shirts_preset = Preset_Builder("Shirt", "Medium", "Fast", "Fast", "No")
presets_list.append(shirts_preset)
pants_preset = Preset_Builder("Pants", "Medium", "Slow", "Slow", "No")
presets_list.append(pants_preset)
socks_preset = Preset_Builder("Socks", "Small", "Fast", "Fast", "Yes")
presets_list.append(socks_preset)
underwear_preset = Preset_Builder("Underwear", "Small", "Fast", "Fast", "Yes")
presets_list.append(underwear_preset)
towel_preset = Preset_Builder("Towel", "Medium", "Fast", "Fast", "Yes")
presets_list.append(towel_preset)
custom_preset = Preset_Builder("Custom", "Large", "Slow", "Fast", "No")
presets_list.append(custom_preset)

# More washing selections
size_water_amount = ["Small", "Medium", "Large"]
agit_speed = ["Fast", "Slow"]
cyc_speed = ["Fast", "Slow"]
soak_item = ["No", "Yes"]

# Keeps track of the choice you're on when pressing on the buttons
press_tracker = 0

# Keep track of the amount of progress each stage has made 
# nump = number progress
intake_nump = 0
agitation_nump = 0
cycle_nump = 0
uv_light_nump = 0
dispense_nump = 0

# Keeps track of when the Progress Bar thread is running
progress_thread_running = True


# Settings Window
# Keeps track of the choices there are which allows you to select through them when clicking on the button
settings_tracker = 0

# Settings Window Values
agitation_slow_speed_range = ["40", "50", "60", "70", "80", "90", "100"]
agitation_fast_speed_range = ["110", "120", "130", "140", "150", "160", "170", "180"]

agitation_slow_duration_range = ["2", "4", "6", "8"]
agitation_fast_duration_range = ["10", "12", "14", "16"]

cycle_slow_speed_range = ["60", "70", "80", "90", "100"]
cycle_fast_speed_range = ["150", "160", "170", "180", "190", "200"]

cycle_slow_duration_range = ["2", "4", "6", "8", "10", "12", "14"]
cycle_fast_duration_range = ["16", "18", "20", "22", "24", "26", "28", "30"]

water_amount_range = ["1000", "1500", "2000", "2500", "3000", "3500", "4000", "4500", "5000", "5500", "6000", "6500", "7000", "7500", "8000", "8500", "9000", "9500", "10000", "10500", "11000", "11500"]

soak_duration_range = ["10", "12", "14", "16", "18", "20", "22", "24"]



# Washing_Machine_GUI
#   Takes care of changing pages (home and settings pages)
class Washing_Machine_GUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		# Initializes Tkinter too basically
		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self, "Washing Machine")
		
		# self.attributes("-fullscreen", True)	
		
		# If the "Escape Key" is hit on keyboard the program ends
		self.bind("<Escape>", exit)
		
		container = tk.Frame(self)
		container.pack()

		self.frames = {}

		for F in (Home_Window, Settings_Window):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(Home_Window)
	
	# show_frame
	#   It raises the frame you want to show the "window"
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()



# Home_Window
#   Everything in the Home Window/Page is within this class
class Home_Window(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.config(background="black")

		# home_date_and_time
		#   Updates to the current time and date every 1 second
		#   A thread is created for it at the bottom of this class
		def home_date_and_time():
			while True:
				now = datetime.now()
				home_date_and_time_text.config(text=now.strftime("%B %d, %Y || %H:%M:%S"))
				time.sleep(1)
		
		# user_press
		#   Makes it for when you click on the button with the choices for washing it shows you your options
		def user_press(current_button, total_selection):
			global press_tracker
			global itemSelection
			global sizeSelection
			global agitationSelection
			global cycleSelection
			global soakSelection
			
			# This changes the other choices based on what the item preset is set to
			if current_button == item_button:
				if press_tracker < len(total_selection):
					# Sets Preset values
					print("Item Button Info/Autofill")
					itemSelection = str(total_selection[press_tracker].item)
					sizeSelection = str(total_selection[press_tracker].size)
					agitationSelection = str(total_selection[press_tracker].agitation)
					cycleSelection = str(total_selection[press_tracker].cycle)
					soakSelection = str(total_selection[press_tracker].soak)
					print(itemSelection)
					print(sizeSelection)
					print(agitationSelection)
					print(cycleSelection)
					print(soakSelection)
					print("---")
					
					current_button.config(text=str(total_selection[press_tracker].item))
					size_button.config(text=str(total_selection[press_tracker].size))
					agitation_button.config(text=str(total_selection[press_tracker].agitation))
					cycle_button.config(text=str(total_selection[press_tracker].cycle))
					soak_button.config(text=str(total_selection[press_tracker].soak))
					press_tracker += 1
				else:
					press_tracker = 0
					
					print("Item Button Info (when end of list is reached):")
					itemSelection = str(total_selection[press_tracker].item)
					sizeSelection = str(total_selection[press_tracker].size)
					agitationSelection = str(total_selection[press_tracker].agitation)
					cycleSelection = str(total_selection[press_tracker].cycle)
					soakSelection = str(total_selection[press_tracker].soak)
					print(itemSelection)
					print(sizeSelection)
					print(agitationSelection)
					print(cycleSelection)
					print(soakSelection)
					print("---")
					
					current_button.config(text=str(total_selection[press_tracker].item))
					size_button.config(text=str(total_selection[press_tracker].size))
					agitation_button.config(text=str(total_selection[press_tracker].agitation))
					cycle_button.config(text=str(total_selection[press_tracker].cycle))
					soak_button.config(text=str(total_selection[press_tracker].soak))
					press_tracker += 1
			# Changes every button on the home page EXCEPT for the Items button
			# The Items button is dealt with in the previous if statement
			elif press_tracker < len(total_selection):
				current_button.config(text=str(total_selection[press_tracker]))
				
				if str(current_button) == ".!frame.!home_window.!button2":
					sizeSelection = str(total_selection[press_tracker])
					print(sizeSelection)
				elif str(current_button) == ".!frame.!home_window.!button3":
					agitationSelection = str(total_selection[press_tracker])
					print(agitationSelection)
				elif str(current_button) == ".!frame.!home_window.!button4":
					cycleSelection = str(total_selection[press_tracker])
					print(cycleSelection)
				elif str(current_button) == ".!frame.!home_window.!button5":
					soakSelection = str(total_selection[press_tracker])
					print(soakSelection)
					
				press_tracker +=1
			else:
				press_tracker = 0
				current_button.config(text=str(total_selection[press_tracker]))
				
				if str(current_button) == ".!frame.!home_window.!button2":
					sizeSelection = str(total_selection[press_tracker])
					print(sizeSelection)
				elif str(current_button) == ".!frame.!home_window.!button3":
					agitationSelection = str(total_selection[press_tracker])
					print(agitationSelection)
				elif str(current_button) == ".!frame.!home_window.!button4":
					cycleSelection = str(total_selection[press_tracker])
					print(cycleSelection)
				elif str(current_button) == ".!frame.!home_window.!button5":
					soakSelection = str(total_selection[press_tracker])
					print(soakSelection)
					
				press_tracker += 1			

		# clear_progressbars
		#   Makes sure that the progress bars are clear
		def clear_progressbars():
			time.sleep(0.5)
			global intake_nump
			global agitation_nump
			global cycle_nump
			global uv_light_nump
			global dispense_nump
			intake_nump = 0
			agitation_nump = 0
			cycle_nump = 0
			uv_light_nump = 0
			dispense_nump = 0
			intake_phase_progress.config(value=intake_nump)
			agitation_phase_progress.config(value=agitation_nump)
			cycle_phase_progress.config(value=cycle_nump)
			uv_light_phase_progress.config(value=uv_light_nump)
			dispense_phase_progress.config(value=dispense_nump)
			self.update_idletasks()

		# artificial_progression
		#   Progresses the progressbar in each stage
		def artificial_progression():
			global intake_nump
			global agitation_nump
			global cycle_nump
			global uv_light_nump
			global dispense_nump
			
			global dateTimeStartIntake
			global itemIntakeLoaded
			global dateTimeStartAgitation
			global waterValveOpened
			#waterAmountML
			global waterLoaded
			global agitationMotorSpeedRPM
			global dateTimeStartSoak
			global waterSalvagedML
			global dateTimeStartCycle
			global cycleMotorSpeedRPM
			global humidityValue
			global temperatureValueC
			global dateTimeStartUVLight
			global uvSelfCheckActive
			global uvLDRCheckActive
			global uvBrightness
			global dateTimeStartDispense
			global itemDispenseUnloaded
			
			
			progess_delay = 0.1
			if progress_thread_running == False:
				print("Pause button pressed")
			elif progress_thread_running == True:
				if intake_nump < 100:
					
					# Get distance sensor data at beginning
					if intake_nump == 0:
						dateTimeStartIntake = Now()
						itemIntakeLoaded, dumby_0 = distanceFunc()
						print("itemIntakeLoaded: ", itemIntakeLoaded)
						
					intake_nump += 10
					intake_phase_progress.config(value=intake_nump)
					self.update_idletasks()
					time.sleep(progess_delay)
					artificial_progression()
				elif agitation_nump < 100:
					
					# Get data at beginning
					if agitation_nump == 0:
						dateTimeStartAgitation = Now()
						waterValveOpened, dumby_1 = servoFunc()
						print("waterValveOpened: ", waterValveOpened)
						if sizeSelection == "Small":
							waterLoaded = int(waterAmountML * 0.2)
						elif sizeSelection == "Medium":
							waterLoaded = int(waterAmountML * 0.6)
						elif sizeSelection == "Large":
							waterLoaded = waterAmountML
						dumby_2, agitationMotorSpeedRPM, dumby_3 = motorFunc(1, agitationSpeedRPM, agitationDurationMIN)
						agitationMotorSpeedRPM = int(agitationMotorSpeedRPM)
					# Get data at ending
					elif agitation_nump == 90:
						if soakSelection == "Yes":
							dateTimeStartSoak = Now()
						elif soakSelection == "No":
							dateTimeStartSoak = "NULL"
						else:
							print("dateTimeStartSoak defining error")
						waterSalvagedML = waterLoaded
						print("waterSalvagedML: ", waterSalvagedML)
					
					agitation_nump += 10
					agitation_phase_progress.config(value=agitation_nump)
					self.update_idletasks()
					time.sleep(progess_delay)
					artificial_progression()
				elif cycle_nump < 100:
					# Get data at beginning
					if cycle_nump == 0:
						dateTimeStartCycle = Now()
						print("dateTimeStartCycle: ", dateTimeStartCycle)
						dumby_4, cycleMotorSpeedRPM, dumby_5 = motorFunc(-1, cycleSpeedRPM, cycleDurationMIN)
						cycleMotorSpeedRPM = int(cycleMotorSpeedRPM)
					# Get data at ending
					elif cycle_nump == 90:
						dumby_6, dumby_7, humidityValue, temperatureValueC = dhtFunc()
						humidityValue = int(humidityValue)
						temperatureValueC = int(temperatureValueC)
					
					cycle_nump += 10
					cycle_phase_progress.config(value=cycle_nump)
					self.update_idletasks()
					time.sleep(progess_delay)
					artificial_progression()
				elif uv_light_nump < 100:
					# Get data at beginning
					if uv_light_nump == 0:
						dateTimeStartUVLight = Now()
						uvSelfCheckActive, uvLDRCheckActive, uvBrightness = lightFunc()
						uvBrightness = int(uvBrightness * 100)
					
					uv_light_nump += 10
					uv_light_phase_progress.config(value=uv_light_nump)
					self.update_idletasks()
					time.sleep(progess_delay)
					artificial_progression()
				elif dispense_nump < 100:
					# Get data at beginning
					if dispense_nump == 0:
						dateTimeStartDispense = Now()
						itemDispenseUnloaded, dumby_8 = distanceFunc()
						print("itemDispenseUnloaded: ", itemDispenseUnloaded)
					# Get data at beginning
					elif dispense_nump == 90:
						# SEND RAW LOG DATA ----------------------------
						sendRawLogData()
						# ----------------------------------------------
					
					dispense_nump += 10
					dispense_phase_progress.config(value=dispense_nump)
					self.update_idletasks()
					time.sleep(progess_delay)
					artificial_progression()
				else:
					start_button.config(text="Start", state="normal", font=TEXT_FONT)
					pause_button.config(state="disable")
					reverse_button.config(state="disable")
					# This thread just clears the progress bars
					clear_progressbars_thread = threading.Thread(target=clear_progressbars, daemon=True)
					clear_progressbars_thread.start()
					clear_progressbars_thread.join()

		# artificial_reverse
		#   Reverses the Washing Machine
		def artificial_reverse():
			global dispense_nump
			global uv_light_nump
			global cycle_nump
			global agitation_nump
			global intake_nump
			degression_delay = 0.1
			if progress_thread_running == False:
				print("Pause button pressed")
			elif progress_thread_running == True:
				if dispense_nump > 0:
					dispense_nump -= 10
					dispense_phase_progress.config(value=dispense_nump)
					self.update_idletasks()
					time.sleep(degression_delay)
					artificial_reverse()
				elif uv_light_nump > 0:
					uv_light_nump -= 10
					uv_light_phase_progress.config(value=uv_light_nump)
					self.update_idletasks()
					time.sleep(degression_delay)
					artificial_reverse()
				elif cycle_nump > 0:
					cycle_nump -= 10
					cycle_phase_progress.config(value=cycle_nump)
					self.update_idletasks()
					time.sleep(degression_delay)
					artificial_reverse()
				elif agitation_nump > 0:
					agitation_nump -= 10
					agitation_phase_progress.config(value=agitation_nump)
					self.update_idletasks()
					time.sleep(degression_delay)
					artificial_reverse()
				elif intake_nump > 0:
					intake_nump -= 10
					intake_phase_progress.config(value=intake_nump)
					self.update_idletasks()
					time.sleep(degression_delay)
					artificial_reverse()
				else:
					start_button.config(text="Start", state="normal", font=TEXT_FONT)
					pause_button.config(state="disable")
					reverse_button.config(state="disabled")
					print("Finished reversing")

		# start_press
		#   Controls what the first/start button does
		def start_press():
			# Creating a starting a thread for the stage progression
			global stage_progression_thread
			global progress_thread_running
			global dataTimeStartPreset
						
			stage_progression_thread = threading.Thread(target=artificial_progression, daemon=True)
			if start_button.cget("text") == "Start":
				start_button.config(text="Resume", state="disabled", font=SMALLER_BUTTON_FONT, pady=10)
				pause_button.config(state="normal")
				reverse_button.config(state="disabled")
				
				# sendRawPresetData ------------------------------------
				dataTimeStartPreset = Now()
				sendRawPresetData()
				# ------------------------------------------------------
				
				stage_progression_thread.start()
			elif start_button.cget("text") == "Resume":
				start_button.config(text="Resume", state="disabled", font=SMALLER_BUTTON_FONT, pady=10)
				pause_button.config(state="normal")
				reverse_button.config(state="disabled")
				progress_thread_running = True
				stage_progression_thread.start()

		# pause_press
		#   Controls what happens when the Pause button is pressed
		def pause_press():
			# Stops the thread from running and it then does .join() to kill it
			try:
				global progress_thread_running
				progress_thread_running = False
				stage_progression_thread.join()
				stage_degression_thread.join()
			except:
				return
			finally:
				start_button.config(state="normal")
				pause_button.config(state="disabled")
				reverse_button.config(state="normal")

		# reverse_press
		#   Controls what happens when the Reverse button is pressed
		def reverse_press():
			global stage_degression_thread
			global progress_thread_running
			start_button.config(state="disabled")
			pause_button.config(state="normal")
			reverse_button.config(state="disabled")
			progress_thread_running = True
			stage_degression_thread = threading.Thread(target=artificial_reverse, daemon=True)
			stage_degression_thread.start()
		
		# shutdown_press
		#	Controls what happens when the Shutdown button is pressed
		def shutdown_press():
			quit()
		
		# Controls the physical buttons on this page
		btn1.when_pressed = lambda: user_press(item_button, presets_list)
		btn2.when_pressed = lambda: user_press(size_button, size_water_amount)
		btn3.when_pressed = lambda: user_press(agitation_button, agit_speed)
		btn4.when_pressed = lambda: user_press(cycle_button, cyc_speed)
		btn5.when_pressed = lambda: user_press(soak_button, soak_item)
		btn6.when_pressed = start_press
		btn7.when_pressed = pause_press
		btn8.when_pressed = reverse_press
		btn9.when_pressed = lambda: controller.show_frame(Settings_Window)
		btn10.when_pressed = shutdown_press
		
		# Creating the Label Widgets for the Text and Buttons
		# Time and Date
		home_date_and_time_text = tk.Label(self, text="Error: Date/Time Not Loaded", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		home_date_and_time_text.grid(row=0, column=2, columnspan=3, padx=(19))

		# Left Side
		# Item Text
		item_text = tk.Label(self, text="Item", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		item_text.grid(row=0, column=0, columnspan=2)
		# Item Button
		item_button = tk.Button(self, text="Custom", font=BUTTON_FONT, command=lambda: user_press(item_button, presets_list))
		item_button.grid(row=1, column=0, columnspan=2)

		# Size Text
		size_text = tk.Label(self, text="Size", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		size_text.grid(row=2, column=0, columnspan=2, pady=(5, 0))
		# Size Button
		size_button = tk.Button(self, text="Large", font=BUTTON_FONT, command=lambda: user_press(size_button, size_water_amount))
		size_button.grid(row=3, column=0, columnspan=2)

		# Agitation Text
		agitation_text = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		agitation_text.grid(row=4, column=0, columnspan=2, pady=(5, 0))
		# Agiation Button
		agitation_button = tk.Button(self, text="Fast", font=BUTTON_FONT, command=lambda: user_press(agitation_button, agit_speed))
		agitation_button.grid(row=5, column=0, columnspan=2)

		# Cycle Text
		cycle_text = tk.Label(self, text="Cycle", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		cycle_text.grid(row=6, column=0, columnspan=2, pady=(5, 0))
		# Cycle Button
		cycle_button = tk.Button(self, text="Slow", font=BUTTON_FONT, command=lambda: user_press(cycle_button, cyc_speed))
		cycle_button.grid(row=7, column=0, columnspan=2)
		
		# Soak Text
		soak_text = tk.Label(self, text="Soak", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		soak_text.grid(row=8, column=0, columnspan=2, pady=(5, 0))
		# Soak Button
		soak_button = tk.Button(self, text="Yes", font=BUTTON_FONT, command=lambda: user_press(soak_button, soak_item))
		soak_button.grid(row=9, column=0, columnspan=2)


		# Right Side
		# Intake Phase Text
		intake_phase_text = tk.Label(self, text="Intake", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		intake_phase_text.grid(row=0, column=5)
		# Intake Phase Progress Bar
		intake_phase_progress = ttk.Progressbar(self)
		intake_phase_progress.grid(row=1, column=5)
		
		# Agitation Phase Text
		agitation_phase_text = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		agitation_phase_text.grid(row=2, column=5)
		# Agitation Phase Progress Bar
		agitation_phase_progress = ttk.Progressbar(self)
		agitation_phase_progress.grid(row=3, column=5)

		# Cycle Phase Text
		cycle_phase_text = tk.Label(self, text="Cycle", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		cycle_phase_text.grid(row=4, column=5)
		# Cycle Phase Progress Bar
		cycle_phase_progress = ttk.Progressbar(self)
		cycle_phase_progress.grid(row=5, column=5)
		
		# UV Light Phase Text
		uv_light_phase_text = tk.Label(self, text="UV Light", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		uv_light_phase_text.grid(row=6, column=5)
		# UV Light Progress Bar
		uv_light_phase_progress = ttk.Progressbar(self)
		uv_light_phase_progress.grid(row=7, column=5)
		
		# Dispense Phase Text
		dispense_phase_text = tk.Label(self, text="Dispense", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		dispense_phase_text.grid(row=8, column=5)
		# Dispense Progress Bar
		dispense_phase_progress = ttk.Progressbar(self)
		dispense_phase_progress.grid(row=9, column=5)


		# Bottom Menu
		# Start Button
		start_button = tk.Button(self, text="Start", font=TEXT_FONT, command=start_press)
		start_button.grid(row=11, column=0, pady=(45, 0), sticky="we")

		# Pause Button
		pause_button = tk.Button(self, text="Pause", font=TEXT_FONT, command=pause_press, state="disabled")
		pause_button.grid(row=11, column=1, pady=(45, 0), sticky="we")

		# Reverse Button
		reverse_button = tk.Button(self, text="Reverse", font=TEXT_FONT, state="disabled", command=reverse_press)
		reverse_button.grid(row=11, column=2, pady=(45, 0), sticky="we")

		# Settings Button
		settings_button = tk.Button(self, text="Settings", font=TEXT_FONT, command=lambda: controller.show_frame(Settings_Window))
		settings_button.grid(row=11, column=3, pady=(45, 0), sticky="e")

		# Shutdown Button
		shutdown_button = tk.Button(self, text="Shutdown", font=TEXT_FONT, command=shutdown_press)
		shutdown_button.grid(row=11, column=5, pady=(45, 0), sticky="e")


		# Creating a thread to allow the date and time to run without being interrupted
		dt_thread = threading.Thread(target=home_date_and_time, daemon=True)
		dt_thread.start()



class Settings_Window(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.config(background="black")

		# settings_date_and_time
		#   Updates to the current time and date every 1 second
		#   A thread is created for it at the bottom of this class
		def settings_date_and_time():
			while True:
				now = datetime.now()
				settings_date_and_time_text.config(text=now.strftime("%B %d, %Y || %H:%M:%S"))
				time.sleep(1)
		
		# user_settings_button_press
		#   Controls what happens when you press on the buttons
		#   It cycles through the choices their are
		def user_settings_button_press(current_button, total_selection, measurement):
			global settings_tracker
			global agitationSpeedRPM
			global agitationDurationMIN
			global cycleMotorSpeedRPM
			global cycleDurationMIN
			global waterAmountML
			global soakDurationMIN
			
			if settings_tracker < len(total_selection):
				current_button.config(text=str(total_selection[settings_tracker])+" "+measurement)
				
				# Grabs agitation speed
				if agitationSelection == "Slow":
					if str(current_button) == ".!frame.!settings_window.!button":
						agitationSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button3":
						agitationDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationDurationMIN)
				elif agitationSelection == "Fast":
					if str(current_button) == ".!frame.!settings_window.!button2":
						agitationSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button4":
						agitationDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationDurationMIN)
				
				# Grabs cycle speed
				if cycleSelection == "Slow":
					if str(current_button) == ".!frame.!settings_window.!button5":
						cycleSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button7":
						cycleDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleDurationMIN)
				elif cycleSelection == "Fast":
					if str(current_button) == ".!frame.!settings_window.!button6":
						cycleSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button8":
						cycleDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleDurationMIN)
						
				# Grabs water amount
				if str(current_button) == ".!frame.!settings_window.!button9":
					waterAmountML = int(current_button.cget("text").split(' ')[0])
					print("waterAmountML", waterAmountML)
				
				if str(current_button) == ".!frame.!settings_window.!button10":
					if soakSelection == "Yes":
						soakDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("soakDurationMIN", soakDurationMIN)
					else:
						soakDurationMIN = 0
				
				settings_tracker +=1
			else:
				settings_tracker = 0
				current_button.config(text=str(total_selection[settings_tracker])+" "+measurement)
				
				# Grabs agitation speed
				if agitationSelection == "Slow":
					if str(current_button) == ".!frame.!settings_window.!button":
						agitationSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button3":
						agitationDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationDurationMIN)
				elif agitationSelection == "Fast":
					if str(current_button) == ".!frame.!settings_window.!button2":
						agitationSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button4":
						agitationDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("agitationSelection:", agitationDurationMIN)
				
				# Grabs cycle speed
				if cycleSelection == "Slow":
					if str(current_button) == ".!frame.!settings_window.!button5":
						cycleSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button7":
						cycleDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleDurationMIN)
				elif cycleSelection == "Fast":
					if str(current_button) == ".!frame.!settings_window.!button6":
						cycleSpeedRPM = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleSpeedRPM)
					elif str(current_button) == ".!frame.!settings_window.!button8":
						cycleDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("cycleSelection:", cycleDurationMIN)
						
				# Grabs water amount
				if str(current_button) == ".!frame.!settings_window.!button9":
					waterAmountML = int(current_button.cget("text").split(' ')[0])
					print("waterAmountML", waterAmountML)
				
				if str(current_button) == ".!frame.!settings_window.!button10":
					if soakSelection == "Yes":
						soakDurationMIN = int(current_button.cget("text").split(' ')[0])
						print("soakDurationMIN", soakDurationMIN)
					else:
						soakDurationMIN = 0
				
				settings_tracker += 1

		# Controls the physical buttons on this page
		'''
		btn1.when_pressed = lambda: user_press(item_button, presets_list)
		btn2.when_pressed = lambda: user_press(size_button, size_water_amount)
		btn3.when_pressed = lambda: user_press(agitation_button, agit_speed)
		btn4.when_pressed = lambda: user_press(cycle_button, cyc_speed)
		btn5.when_pressed = lambda: user_press(soak_button, soak_item)
		btn6.when_pressed = start_press
		btn7.when_pressed = pause_press
		btn8.when_pressed = reverse_press
		btn9.when_pressed = lambda: controller.show_frame(Settings_Window)
		btn10.when_pressed = shutdown_press
		'''

		# Creating the Label Widgets for the text and button
		# Time and Date
		settings_date_and_time_text = tk.Label(self, text="Error: Date/Time Not Loaded", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		settings_date_and_time_text.grid(row=0, column=1, columnspan=3, padx=(74, 19))

		# Agitation Section
		agitation_section = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		agitation_section.grid(row=1, column=0, columnspan=2, pady=(10, 0))
		# Slow Agitation Speed Text
		slow_agitation_speed_text = tk.Label(self, text="Slow Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		slow_agitation_speed_text.grid(row=2, column=0)
		# Slow Agitation Speed Button
		slow_agitation_speed_button = tk.Button(self, text="40 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_agitation_speed_button, agitation_slow_speed_range, "RPM"))
		slow_agitation_speed_button.grid(row=3, column=0)
		
		# Fast Agitation Speed Text
		fast_agitation_speed_text = tk.Label(self, text="Fast Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		fast_agitation_speed_text.grid(row=2, column=1)
		# Fast Agitation Speed Button
		fast_agitation_speed_button = tk.Button(self, text="110 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_agitation_speed_button, agitation_fast_speed_range, "RPM"))
		fast_agitation_speed_button.grid(row=3, column=1)
		
		# Slow Agitation Duration Text
		slow_agitation_duration_text = tk.Label(self, text="Slow Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		slow_agitation_duration_text.grid(row=4, column=0)
		# Slow Agitation Duration Button
		slow_agitation_duration_button = tk.Button(self, text="2 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_agitation_duration_button, agitation_slow_duration_range, "MIN"))
		slow_agitation_duration_button.grid(row=5, column=0)
		
		# Fast Agitation Duration Text
		fast_agitation_duration_text = tk.Label(self, text="Fast Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		fast_agitation_duration_text.grid(row=4, column=1)
		# Fast Agitation Duration Button
		fast_agitation_duration_button = tk.Button(self, text="10 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_agitation_duration_button, agitation_fast_duration_range, "MIN"))
		fast_agitation_duration_button.grid(row=5, column=1)


		# Cycle Section
		cycle_section = tk.Label(self, text="Cycle", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		cycle_section.grid(row=6, column=0, columnspan=2, pady=(23, 0), padx=(0, 30))
		# Slow Cycle Speed Text
		slow_cycle_speed_text = tk.Label(self, text="Slow Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		slow_cycle_speed_text.grid(row=7, column=0)
		# Slow Cycle Speed Button
		slow_cycle_speed_button = tk.Button(self, text="60 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_cycle_speed_button, cycle_slow_speed_range, "RPM"))
		slow_cycle_speed_button.grid(row=8, column=0)

		# Fast Cycle Speed Text
		fast_cycle_speed_text = tk.Label(self, text="Fast Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		fast_cycle_speed_text.grid(row=7, column=1)
		# Fast Cycle Speed Button
		fast_cycle_speed_button = tk.Button(self, text="150 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_cycle_speed_button, cycle_fast_speed_range, "RPM"))
		fast_cycle_speed_button.grid(row=8, column=1)

		# Slow Cycle Duration Text
		slow_cycle_duration_text = tk.Label(self, text="Slow Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		slow_cycle_duration_text.grid(row=9, column=0)
		# Slow Cycle Duration Button
		slow_cycle_duration_button = tk.Button(self, text="2 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_cycle_duration_button, cycle_slow_duration_range, "MIN"))
		slow_cycle_duration_button.grid(row=10, column=0)

		# Fast Cycle Duration Text
		fast_cycle_duration_text = tk.Label(self, text="Fast Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		fast_cycle_duration_text.grid(row=9, column=1)
		# Fast Cycle Duration Button
		fast_cycle_duration_button = tk.Button(self, text="16 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_cycle_duration_button, cycle_fast_duration_range, "MIN"))
		fast_cycle_duration_button.grid(row=10, column=1)

		
		# Water Amount Text
		water_amount_text = tk.Label(self, text="Water Amount", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		water_amount_text.grid(row=2, column=2, columnspan=2)
		# Water Amount Button
		water_amount_button = tk.Button(self, text="1000 ML", font=BUTTON_FONT, command=lambda: user_settings_button_press(water_amount_button, water_amount_range, "ML"))
		water_amount_button.grid(row=3, column=2, columnspan=2) 

		
		# Soak Duration Text
		soak_duration_text = tk.Label(self, text="Soak Duration", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
		soak_duration_text.grid(row=7, column=2, columnspan=2)
		# Soak Duration Button
		soak_duration_button = tk.Button(self, text="10 MIN", font=BUTTON_FONT, command=lambda: user_settings_button_press(soak_duration_button, soak_duration_range, "MIN"))
		soak_duration_button.grid(row=8, column=2, columnspan=2) 


		# Buttom Menu
		# Home Button
		home_button = tk.Button(self, text="Home", font=TEXT_FONT, command=lambda: controller.show_frame(Home_Window))
		home_button.grid(row=11, column=2, pady=(24, 0), sticky="e")

		# Shutdown Button
		shutdown_button = tk.Button(self, text="Shutdown", font=TEXT_FONT, command=quit)
		shutdown_button.grid(row=11, column=4, pady=(24, 0), sticky="e")


		# Creating a thread to allow the date and time to run without being interrupted
		dt_thread = threading.Thread(target=settings_date_and_time, daemon=True)
		dt_thread.start()



# Starts the GUI
Washing_Machine_GUI().mainloop()
