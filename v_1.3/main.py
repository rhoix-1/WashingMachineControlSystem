import time
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# import data

# Data Values
# Ethans Stuff ---
LightToggle = ["Off", "On"]
MotorToggle = ["Off", "On"]
PumpToggle = ["Off", "On"]
ValveToggle = ["Closed", "Open"]
# ---


agitation_slow = [30, 35, 40, 45]
agitation_fast = []

cycle_duration_slow = []
cycle_duration_fast = []

water_amount = 1

soak_duration = 1


# Text/Button Design
TEXT_FONT = ("Roboto", 20)
TEXT_COLOR = "white"
TEXT_BACKGROUND_COLOR = "black"
BUTTON_FONT = ("Roboto", 15)

SMALLER_FONT = ("Roboto", 15)
SMALLER_BUTTON_FONT = ("Roboto", 12)

# Keeps track of the choices there are which allows you to select through them when clicking on the button

settings_tracker = 0


# Settings Page Values
agitation_slow_speed_range = ["100", "150", "200", "250", "300", "350", "400"]
agitation_fast_speed_range = ["450", "500", "550", "600", "650", "700", "750", "800"]

agitation_slow_duration_range = ["2", "4", "6", "8"]
agitation_fast_duration_range = ["10", "12", "14", "16"]

cycle_slow_speed_range = ["900", "925", "950", "975", "1000"]
cycle_fast_speed_range = ["1025", "1050", "1100", "1125", "1150", "1200"]

cycle_slow_duration_range = ["2", "4", "6", "8", "10", "12", "14"]
cycle_fast_duration_range = ["16", "18", "20", "22", "24", "26", "28", "30"]

water_amount_range = ["10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100", "105", "110", "115"]

soak_duration_range = ["25", "30", "35", "40", "45", "50", "55", "60"]


'''
itemIntakeLoaded, itemDistance = data.distanceFunc()
waterValeOpened, servoAngle = data.servoFunc()
motorDirection, agitationMotorSpeedRPM, motorDuration = data.motorFunc(1, 60, 5)
motorDirection, cycleMotorSpeedRPM, motorDuration = data.motorFunc(-1, 10, 5)
internalHumid, internalTemp, humidity, temperatureC = data.dhtFunc()
uvSelfCheck, uvLDRCheck, uvBrightness = data.lightFunc()

# Need to make a function to get fake values for: waterLevelML, waterLoaded, waterSalvagedML
'''

# -------------------------------





# Home Window
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
draining_nump = 0
uv_light_nump = 0
dispense_nump = 0

# Keeps track of when the Progress Bar thread is running
progress_thread_running = True


# Settings Window



# Washing_Machine_GUI
#   Takes care of changing pages (home and settings pages)
class Washing_Machine_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Initializes Tkinter too basically
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default="images/j.ico")
        tk.Tk.wm_title(self, "Washing Machine")

        self.geometry("800x480")

        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        for F in (Home_Window, Settings_Window):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home_Window)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Home_Window
#   Everything in the Home Window/Page is within this class
class Home_Window(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background="black")

        # date_and_time
        #   Updates to the current time and date every 1 second
        #   A thread is created for it at the bottom of this class
        def date_and_time():
            while True:
                now = datetime.now()
                date_and_time_text.config(text=now.strftime("%B %d, %Y || %H:%M:%S"))
                time.sleep(1)
        
        # user_press
        #   Makes it for when you click on the button with the choices for washing it shows you your options
        def user_press(current_button, total_selection):
            global press_tracker
            # This changes the other choices based on what the item preset is set to
            if current_button == item_button:
                if press_tracker < len(total_selection):
                    current_button.config(text=str(total_selection[press_tracker].item))
                    size_button.config(text=str(total_selection[press_tracker].size))
                    agitation_button.config(text=str(total_selection[press_tracker].agitation))
                    cycle_button.config(text=str(total_selection[press_tracker].cycle))
                    soak_button.config(text=str(total_selection[press_tracker].soak))
                    press_tracker += 1
                else:
                    press_tracker = 0
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
                press_tracker +=1
            else:
                press_tracker = 0
                current_button.config(text=str(total_selection[press_tracker]))
                press_tracker += 1

        # clear_progressbars
        #   Makes sure that the progress bars are clear
        def clear_progressbars():
            time.sleep(0.5)
            global intake_nump
            global agitation_nump
            global draining_nump
            global uv_light_nump
            global dispense_nump
            intake_nump = 0
            agitation_nump = 0
            draining_nump = 0
            uv_light_nump = 0
            dispense_nump = 0
            intake_phase_progress.config(value=intake_nump)
            agitation_phase_progress.config(value=agitation_nump)
            draining_phase_progress.config(value=draining_nump)
            uv_light_phase_progress.config(value=uv_light_nump)
            dispense_phase_progress.config(value=dispense_nump)
            self.update_idletasks()

        # artificial_progression
        #   Progresses the progressbar in each stage
        def artificial_progression():
            global intake_nump
            global agitation_nump
            global draining_nump
            global uv_light_nump
            global dispense_nump
            progess_delay = 0.1
            if progress_thread_running == False:
                print("Pause button pressed")
            elif progress_thread_running == True:
                if intake_nump < 100:
                    intake_nump += 10
                    intake_phase_progress.config(value=intake_nump)
                    self.update_idletasks()
                    time.sleep(progess_delay)
                    artificial_progression()
                elif agitation_nump < 100:
                    agitation_nump += 10
                    agitation_phase_progress.config(value=agitation_nump)
                    self.update_idletasks()
                    time.sleep(progess_delay)
                    artificial_progression()
                elif draining_nump < 100:
                    draining_nump += 10
                    draining_phase_progress.config(value=draining_nump)
                    self.update_idletasks()
                    time.sleep(progess_delay)
                    artificial_progression()
                elif uv_light_nump < 100:
                    uv_light_nump += 10
                    uv_light_phase_progress.config(value=uv_light_nump)
                    self.update_idletasks()
                    time.sleep(progess_delay)
                    artificial_progression()
                elif dispense_nump < 100:
                    dispense_nump += 10
                    dispense_phase_progress.config(value=dispense_nump)
                    self.update_idletasks()
                    time.sleep(progess_delay)
                    artificial_progression()
                else:
                    start_button.config(text="Start", state="normal")
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
            global draining_nump
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
                elif draining_nump > 0:
                    draining_nump -= 10
                    draining_phase_progress.config(value=draining_nump)
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
                    start_button.config(text="Start", state="normal")
                    pause_button.config(state="disable")
                    reverse_button.config(state="disabled")
                    print("Finished reversing")

        # start_press
        #   Controls what the first/start button does
        def start_press():
            # Creating a starting a thread for the stage progression
            global stage_progression_thread
            global progress_thread_running
            stage_progression_thread = threading.Thread(target=artificial_progression, daemon=True)
            if start_button.cget("text") == "Start":
                '''
                # Instantly Clears the Progress Bars
                global intake_nump
                global agitation_nump
                global draining_nump
                global uv_light_nump
                global dispense_nump
                intake_nump = 0
                agitation_nump = 0
                draining_nump = 0
                uv_light_nump = 0
                dispense_nump = 0
                intake_phase_progress.config(value=intake_nump)
                agitation_phase_progress.config(value=agitation_nump)
                draining_phase_progress.config(value=draining_nump)
                uv_light_phase_progress.config(value=uv_light_nump)
                dispense_phase_progress.config(value=dispense_nump)
                self.update_idletasks()
                '''
                start_button.config(text="Resume", state="disabled")
                pause_button.config(state="normal")
                reverse_button.config(state="disabled")
                stage_progression_thread.start()
            elif start_button.cget("text") == "Resume":
                start_button.config(text="Resume", state="disabled")
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
        #   Controls what happens when the Reverse button is presses
        def reverse_press():
            global stage_degression_thread
            global progress_thread_running
            start_button.config(state="disabled")
            pause_button.config(state="normal")
            reverse_button.config(state="disabled")
            progress_thread_running = True
            stage_degression_thread = threading.Thread(target=artificial_reverse, daemon=True)
            stage_degression_thread.start()

        # Creating the Label Widgets for the Text and Buttons
        # Time and Date
        date_and_time_text = tk.Label(self, text="Error: Date/Time Not Loaded", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        date_and_time_text.grid(row=0, column=2, columnspan=3, padx=(56, 50))

        # Left Side
        # Item Text
        item_text = tk.Label(self, text="Item", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        item_text.grid(row=0, column=0, columnspan=2)
        # Item Button
        item_button = tk.Button(self, text="Custom", font=BUTTON_FONT, command=lambda: user_press(item_button, presets_list))
        item_button.grid(row=1, column=0, columnspan=2)

        # Size Text
        size_text = tk.Label(self, text="Size", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        size_text.grid(row=2, column=0, columnspan=2)
        # Size Button
        size_button = tk.Button(self, text="Large", font=BUTTON_FONT, command=lambda: user_press(size_button, size_water_amount))
        size_button.grid(row=3, column=0, columnspan=2)

        # Agitation Text
        agitation_text = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        agitation_text.grid(row=4, column=0, columnspan=2)
        # Agiation Button
        agitation_button = tk.Button(self, text="Fast", font=BUTTON_FONT, command=lambda: user_press(agitation_button, agit_speed))
        agitation_button.grid(row=5, column=0, columnspan=2)

        # Cycle Text
        cycle_text = tk.Label(self, text="Cycle", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        cycle_text.grid(row=6, column=0, columnspan=2)
        # Cycle Button
        cycle_button = tk.Button(self, text="Slow", font=BUTTON_FONT, command=lambda: user_press(cycle_button, cyc_speed))
        cycle_button.grid(row=7, column=0, columnspan=2)
        
        # Soak Text
        soak_text = tk.Label(self, text="Soak", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        soak_text.grid(row=8, column=0, columnspan=2)
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

        # Draining Phase Text
        draining_phase_text = tk.Label(self, text="Draining", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        draining_phase_text.grid(row=4, column=5)
        # Draining Phase Progress Bar
        draining_phase_progress = ttk.Progressbar(self)
        draining_phase_progress.grid(row=5, column=5)
        
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
        start_button.grid(row=11, column=0, pady=(35, 0), sticky="we")

        # Pause Button
        pause_button = tk.Button(self, text="Pause", font=TEXT_FONT, command=pause_press, state="disabled")
        pause_button.grid(row=11, column=1, pady=(35, 0), sticky="we")

        # Reverse Button
        reverse_button = tk.Button(self, text="Reverse", font=TEXT_FONT, state="disabled", command=reverse_press)
        reverse_button.grid(row=11, column=2, pady=(35, 0), sticky="we")

        # Settings Button
        settings_button = tk.Button(self, text="Settings", font=TEXT_FONT, command=lambda: controller.show_frame(Settings_Window))
        settings_button.grid(row=11, column=3, pady=(35, 0), sticky="e")

        # Shutdown Button
        shutdown_button = tk.Button(self, text="Shutdown", font=TEXT_FONT, command=quit)
        shutdown_button.grid(row=11, column=5, pady=(35, 0), sticky="e")


        # Creating a thread to allow the date and time to run without being interrupted
        dt_thread = threading.Thread(target=date_and_time, daemon=True)
        dt_thread.start()



class Settings_Window(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background="black")

        def date_and_time():
            now = datetime.now()
            date_and_time_text.config(text=now.strftime("%B %d, %Y || %H:%M:%S"))
            date_and_time_text.after(1000, date_and_time)


        def user_settings_button_press(current_button, total_selection, measurement):
            global settings_tracker
            if settings_tracker < len(total_selection):
                current_button.config(text=str(total_selection[settings_tracker])+" "+measurement)
                settings_tracker +=1
            else:
                settings_tracker = 0
                current_button.config(text=str(total_selection[settings_tracker])+" "+measurement)
                settings_tracker += 1

        # Creating the Label Widgets for the text and button
        # Settings Window/Frame

        # Time and Date
        date_and_time_text = tk.Label(self, text="Error: Date/Time Not Loaded", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        date_and_time_text.grid(row=0, column=1, columnspan=3, padx=(110, 50))


        # Agitation Section
        agitation_section = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        agitation_section.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        # Slow Agitation Speed Text
        slow_agitation_speed_text = tk.Label(self, text="Slow Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        slow_agitation_speed_text.grid(row=2, column=0)
        # Slow Agitation Speed Button
        slow_agitation_speed_button = tk.Button(self, text="100 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_agitation_speed_button, agitation_slow_speed_range, "RPM"))
        slow_agitation_speed_button.grid(row=3, column=0)
        
        # Fast Agitation Speed Text
        fast_agitation_speed_text = tk.Label(self, text="Fast Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        fast_agitation_speed_text.grid(row=2, column=1)
        # Fast Agitation Speed Button
        fast_agitation_speed_button = tk.Button(self, text="450 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_agitation_speed_button, agitation_fast_speed_range, "RPM"))
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
        slow_cycle_speed_button = tk.Button(self, text="900 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_cycle_speed_button, cycle_slow_speed_range, "RPM"))
        slow_cycle_speed_button.grid(row=8, column=0)

        # Fast Cycle Speed Text
        fast_cycle_speed_text = tk.Label(self, text="Fast Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        fast_cycle_speed_text.grid(row=7, column=1)
        # Fast Cycle Speed Button
        fast_cycle_speed_button = tk.Button(self, text="1025 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_cycle_speed_button, cycle_fast_speed_range, "RPM"))
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
        water_amount_button = tk.Button(self, text="10 L", font=BUTTON_FONT, command=lambda: user_settings_button_press(water_amount_button, water_amount_range, "L"))
        water_amount_button.grid(row=3, column=2, columnspan=2) 

        
        # Soak Duration Text
        soak_duration_text = tk.Label(self, text="Soak Duration", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        soak_duration_text.grid(row=7, column=2, columnspan=2)
        # Soak Duration Button
        soak_duration_button = tk.Button(self, text="25 MIN", font=BUTTON_FONT, command=lambda: user_settings_button_press(soak_duration_button, soak_duration_range, "MIN"))
        soak_duration_button.grid(row=8, column=2, columnspan=2) 


        # Home Button
        home_button = tk.Button(self, text="Home", font=TEXT_FONT, command=lambda: controller.show_frame(Home_Window))
        home_button.grid(row=11, column=2, padx=(10, 0), sticky="e")
        # Shutdown Button
        shutdown_button = tk.Button(self, text="Shutdown", font=TEXT_FONT, command=quit)
        shutdown_button.grid(row=11, column=4, sticky="e")


        # Calls the function that keeps the clock going in the settings window
        date_and_time()
        

# Starts the GUI
Washing_Machine_GUI().mainloop()