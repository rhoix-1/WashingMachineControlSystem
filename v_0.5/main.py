# Platt Tech Nasa Hunch Team (Ethan Feldman & Josepher Shunaula)
import kivy
import time
import dataCollector
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen


# Sends Data
dataCollector.SendData()


# This variable keeps track when you go through your choices
selectionCounter = 0

class HomeWindow(Screen):
    # userInputSelections
    #   This function is what allows you to select through you choices
    def userInputSelections(self, currentSelection, totalSelection):
        global selectionCounter
        totalSelection = eval(totalSelection)
        if selectionCounter < len(totalSelection):
            currentSelection.text = str(totalSelection[selectionCounter])
            selectionCounter += 1
        else:
            selectionCounter = 0
            currentSelection.text = str(totalSelection[selectionCounter])
            selectionCounter += 1
            

class SettingsWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class WashingMachineUI(App):
    def build(self):
        return


if __name__ == "__main__":
    WashingMachineUI().run()

