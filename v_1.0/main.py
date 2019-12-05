from tkinter import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.home_window()
    
    def home_window(self):
        self.master.title("Washing Machine")

        # Creating the Label Widgets for the text
        item_text = Label(self, text="Item")
        size_text = Label(self, text="Size")
        agitation_speed_text = Label(self, text="Agitation Speed")
        cycle_duration_text = Label(self, text="Cycle Duration")
        soak_text = Label(self, text="Soak")

        intake_phase_text = Label(self, text="Intake")
        agitation_phase_text = Label(self, text="Agitation")
        draining_phase_text = Label(self, text="Draining")
        uv_light_phase_text = Label(self, text="UV Light")
        dispense_phase_text = Label(self, text="Dispense")

        text = Label(self, text="hi, i'm steve")
        text.pack()
        
        '''
        item_text.grid(row=0, column=0)
        size_text.grid(row=0, column=3)
        agitation_speed_text.grid(row=0, column=5)
        '''

root = Tk()
root.geometry("800x480")
app = Window(root)
root.mainloop()