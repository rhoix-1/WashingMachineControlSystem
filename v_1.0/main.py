import time
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Data Values
itemOfClothing = ["Shirt", "Pants", "Sock", "Underwear", "Towel", "Custom"]
waterAmount = ["Small", "Medium", "Large"]
aSpeed = ["Fast", "Slow"]
cSpeed = ["Fast", "Slow"]
soakItem = ["No", "Yes"]

LightToggle = ["Off", "On"]
MotorToggle = ["Off", "On"]
PumpToggle = ["Off", "On"]
ValveToggle = ["Closed", "Open"]

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
preset_tracker = 0
settings_tracker = 0

# Keeps a number to track the progress of each stage (nump = number progress)
intake_nump = 0
agitation_nump = 0
draining_nump = 0
uv_light_nump = 0
dispense_nump = 0


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

class Washing_Machine_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Initializes Tkinter too basically
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self, default="images/j.ico")
        tk.Tk.wm_title(self, "Washing Machine")

        self.geometry("800x480")

        print(self.winfo_screenheight())

        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        for F in (HomeWindow, SettingsWindow):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomeWindow)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomeWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background="black")

        def date_and_time():
            now = datetime.now()
            date_and_time_text.config(text=now.strftime("%B %d, %Y || %H:%M:%S"))
            date_and_time_text.after(1000, date_and_time)
        
        def presets_change(total_selection):
            def selection_change(size, ag_speed, cy_duration, if_soak):
                size_button.config(text=size)
                agitation_speed_button.config(text=ag_speed)
                cycle_speed_button.config(text=cy_duration)
                soak_button.config(text=if_soak)

            if total_selection[preset_tracker] == "Shirt":
                print("Shirt Preset Selected")
                selection_change("Medium", "Fast", "Fast", "No")
            elif total_selection[preset_tracker] == "Pants":
                print("Pants Preset Selected")
                selection_change("Medium", "Slow", "Slow", "No")
            elif total_selection[preset_tracker] == "Sock":
                print("Sock Preset Selected")
                selection_change("Small", "Fast", "Fast", "Yes")
            elif total_selection[preset_tracker] == "Underwear":
                print("Underwear Preset Selected")
                selection_change("Small", "Fast", "Fast", "Yes")
            elif total_selection[preset_tracker] == "Towel":
                print("Towel Preset Selected")
                selection_change("Medium", "Fast", "Fast", "Yes")
            elif total_selection[preset_tracker] == "Custom":
                print("Custom")

        def user_item_button_press(current_button, total_selection):
            global preset_tracker
            if preset_tracker < len(total_selection):
                current_button.config(text=str(total_selection[preset_tracker]))
                presets_change(total_selection)
                preset_tracker +=1
            else:
                preset_tracker = 0
                current_button.config(text=str(total_selection[preset_tracker]))
                presets_change(total_selection)
                preset_tracker += 1

        def start_pressed():
            global intake_nump
            global agitation_nump
            global draining_nump
            global uv_light_nump
            global dispense_nump
            start_button.config(state="disabled")
            # Artificial Process
            if intake_nump < 100:
                intake_nump += 10
                intake_phase_progress.config(value=intake_nump)
                self.update_idletasks()
                time.sleep(0.5)
                date_and_time()
                start_pressed()
            elif agitation_nump < 100:
                agitation_nump += 10
                agitation_phase_progress.config(value=agitation_nump)
                self.update_idletasks()
                time.sleep(0.5)
                date_and_time()
                start_pressed()
            elif draining_nump < 100:
                draining_nump += 10
                draining_phase_progress.config(value=draining_nump)
                self.update_idletasks()
                time.sleep(0.5)
                date_and_time()
                start_pressed()
            elif uv_light_nump < 100:
                uv_light_nump += 10
                uv_light_phase_progress.config(value=uv_light_nump)
                self.update_idletasks()
                time.sleep(0.5)
                date_and_time()
                start_pressed()
            elif dispense_nump < 100:
                dispense_nump += 10
                dispense_phase_progress.config(value=dispense_nump)
                self.update_idletasks()
                time.sleep(0.5)
                date_and_time()
                start_pressed()
            else:
                start_button.config(state="normal")
                print("ALL DONE")

        def pause_pressed():
            reverse_button.config(state="normal")


        # Creating the Label Widgets for the text and buttons
        # Time and Date
        date_and_time_text = tk.Label(self, text="Error: Date/Time Not Loaded", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        # Left Side
        item_text = tk.Label(self, text="Item", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        item_button = tk.Button(self, text="Towel", font=BUTTON_FONT, command=lambda: user_item_button_press(item_button, itemOfClothing))
        
        size_text = tk.Label(self, text="Size", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        size_button = tk.Button(self, text="Large", font=BUTTON_FONT, command=lambda: user_item_button_press(size_button, waterAmount))
        
        agitation_speed_text = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        agitation_speed_button = tk.Button(self, text="Fast", font=BUTTON_FONT, command=lambda: user_item_button_press(agitation_speed_button, aSpeed))
        
        cycle_speed_text = tk.Label(self, text="Cycle", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        cycle_speed_button = tk.Button(self, text="Slow", font=BUTTON_FONT, command=lambda: user_item_button_press(cycle_speed_button, cSpeed))
        
        soak_text = tk.Label(self, text="Soak", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        soak_button = tk.Button(self, text="Yes", font=BUTTON_FONT, command=lambda: user_item_button_press(soak_button, soakItem))
        # Right Side
        intake_phase_text = tk.Label(self, text="Intake", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        intake_phase_progress = ttk.Progressbar(self)
        
        agitation_phase_text = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        agitation_phase_progress = ttk.Progressbar(self)
        
        draining_phase_text = tk.Label(self, text="Draining", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        draining_phase_progress = ttk.Progressbar(self)
        
        uv_light_phase_text = tk.Label(self, text="UV Light", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        uv_light_phase_progress = ttk.Progressbar(self)
        
        dispense_phase_text = tk.Label(self, text="Dispense", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        dispense_phase_progress = ttk.Progressbar(self)
        # Bottom Menu
        start_button = tk.Button(self, text="Start", font=TEXT_FONT, command=start_pressed)
        pause_button = tk.Button(self, text="Pause", font=TEXT_FONT, command=pause_pressed)
        reverse_button = tk.Button(self, text="Reverse", font=TEXT_FONT, state="disabled")
        settings_button = tk.Button(self, text="Settings", font=TEXT_FONT, command=lambda: controller.show_frame(SettingsWindow))
        shutdown_button = tk.Button(self, text="Shutdown", font=TEXT_FONT, command=quit)

        # Putting it in the Frame using a Grid
        # Top Time and Date
        date_and_time_text.grid(row=0, column=2, columnspan=3, padx=(56, 50))
        # Left Side
        item_text.grid(row=0, column=0, columnspan=2)
        item_button.grid(row=1, column=0, columnspan=2)
        
        size_text.grid(row=2, column=0, columnspan=2)
        size_button.grid(row=3, column=0, columnspan=2)
        
        agitation_speed_text.grid(row=4, column=0, columnspan=2)
        agitation_speed_button.grid(row=5, column=0, columnspan=2)
        
        cycle_speed_text.grid(row=6, column=0, columnspan=2)
        cycle_speed_button.grid(row=7, column=0, columnspan=2)
        
        soak_text.grid(row=8, column=0, columnspan=2)
        soak_button.grid(row=9, column=0, columnspan=2)
        # Right Side
        intake_phase_text.grid(row=0, column=5)
        intake_phase_progress.grid(row=1, column=5)
        
        agitation_phase_text.grid(row=2, column=5)
        agitation_phase_progress.grid(row=3, column=5)
        
        draining_phase_text.grid(row=4, column=5)
        draining_phase_progress.grid(row=5, column=5)
        
        uv_light_phase_text.grid(row=6, column=5)
        uv_light_phase_progress.grid(row=7, column=5)
        
        dispense_phase_text.grid(row=8, column=5)
        dispense_phase_progress.grid(row=9, column=5)
        # Button Menu
        start_button.grid(row=11, column=0, pady=(35, 0), sticky="we")
        pause_button.grid(row=11, column=1, pady=(35, 0), sticky="we")
        reverse_button.grid(row=11, column=2, pady=(35, 0), sticky="we")
        settings_button.grid(row=11, column=3, pady=(35, 0), sticky="e")
        shutdown_button.grid(row=11, column=5, pady=(35, 0), sticky="e")
        # Calls the function that keeps the clock going in the home window
        date_and_time()


class SettingsWindow(tk.Frame):
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

        # Time and Date -------
        date_and_time_text = tk.Label(self, text="Error: Date/Time Not Loaded", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        
        # Agitation Section ---
        agitation_section = tk.Label(self, text="Agitation", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)

        slow_agitation_speed_text = tk.Label(self, text="Slow Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        slow_agitation_speed_button = tk.Button(self, text="100 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_agitation_speed_button, agitation_slow_speed_range, "RPM"))
        fast_agitation_speed_text = tk.Label(self, text="Fast Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        fast_agitation_speed_button = tk.Button(self, text="450 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_agitation_speed_button, agitation_fast_speed_range, "RPM"))

        slow_agitation_duration_text = tk.Label(self, text="Slow Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        slow_agitation_duration_button = tk.Button(self, text="2 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_agitation_duration_button, agitation_slow_duration_range, "MIN"))
        fast_agitation_duration_text = tk.Label(self, text="Fast Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        fast_agitation_duration_button = tk.Button(self, text="10 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_agitation_duration_button, agitation_fast_duration_range, "MIN"))
        # Cycle Section -------
        cycle_section = tk.Label(self, text="Cycle", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        slow_cycle_speed_text = tk.Label(self, text="Slow Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        slow_cycle_speed_button = tk.Button(self, text="900 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_cycle_speed_button, cycle_slow_speed_range, "RPM"))
        fast_cycle_speed_text = tk.Label(self, text="Fast Speed", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        fast_cycle_speed_button = tk.Button(self, text="1025 RPM", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_cycle_speed_button, cycle_fast_speed_range, "RPM"))
    
        slow_cycle_duration_text = tk.Label(self, text="Slow Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        slow_cycle_duration_button = tk.Button(self, text="2 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(slow_cycle_duration_button, cycle_slow_duration_range, "MIN"))
        fast_cycle_duration_text = tk.Label(self, text="Fast Duration", font=SMALLER_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        fast_cycle_duration_button = tk.Button(self, text="16 MIN", font=SMALLER_BUTTON_FONT, command=lambda: user_settings_button_press(fast_cycle_duration_button, cycle_fast_duration_range, "MIN"))
        # Water Section -------
        water_amount_text = tk.Label(self, text="Water Amount", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        water_amount_button = tk.Button(self, text="10 L", font=BUTTON_FONT, command=lambda: user_settings_button_press(water_amount_button, water_amount_range, "L"))
        # Soak Duration -------
        soak_duration_text = tk.Label(self, text="Soak Duration", font=TEXT_FONT, background=TEXT_BACKGROUND_COLOR, foreground=TEXT_COLOR)
        soak_duration_button = tk.Button(self, text="25 MIN", font=BUTTON_FONT, command=lambda: user_settings_button_press(soak_duration_button, soak_duration_range, "MIN"))
        # Bottom Nav. Buttons -
        home_button = tk.Button(self, text="Home", font=TEXT_FONT, command=lambda: controller.show_frame(HomeWindow))
        shutdown_button = tk.Button(self, text="Shutdown", font=TEXT_FONT, command=quit)


        # Putting it in the Frame using a Grid

        # Time and Date -------
        date_and_time_text.grid(row=0, column=1, columnspan=3, padx=(110, 50))
        
        # Agitation Section ---
        agitation_section.grid(row=1, column=0, columnspan=2, pady=(10, 0))
    
        slow_agitation_speed_text.grid(row=2, column=0)
        slow_agitation_speed_button.grid(row=3, column=0)
        fast_agitation_speed_text.grid(row=2, column=1)
        fast_agitation_speed_button.grid(row=3, column=1)

        slow_agitation_duration_text.grid(row=4, column=0)
        slow_agitation_duration_button.grid(row=5, column=0)
        fast_agitation_duration_text.grid(row=4, column=1)
        fast_agitation_duration_button.grid(row=5, column=1)
        # Cycle Section -------
        cycle_section.grid(row=6, column=0, columnspan=2, pady=(23, 0), padx=(0, 30))

        slow_cycle_speed_text.grid(row=7, column=0)
        slow_cycle_speed_button.grid(row=8, column=0)
        fast_cycle_speed_text.grid(row=7, column=1)
        fast_cycle_speed_button.grid(row=8, column=1)

        slow_cycle_duration_text.grid(row=9, column=0)
        slow_cycle_duration_button.grid(row=10, column=0)
        fast_cycle_duration_text.grid(row=9, column=1)
        fast_cycle_duration_button.grid(row=10, column=1)
        # Water Section -------
        water_amount_text.grid(row=2, column=2, columnspan=2)
        water_amount_button.grid(row=3, column=2, columnspan=2)   
        # Soak Section --------
        soak_duration_text.grid(row=7, column=2, columnspan=2)
        soak_duration_button.grid(row=8, column=2, columnspan=2)     
        # Bottom Nav. Buttons -
        home_button.grid(row=11, column=2, padx=(10, 0), sticky="e")
        shutdown_button.grid(row=11, column=4, sticky="e")

        # Calls the function that keeps the clock going in the settings window
        date_and_time()
        

# Starts the GUI
Washing_Machine_GUI().mainloop()