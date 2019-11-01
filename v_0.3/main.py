# Platt Tech Nasa Hunch Team (Josepher Shunaula & Ethan Feldman)
import kivy
import dataCollector
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

''' 
# Connection To Backend
import dataCollector
dataCollector.SendData()
'''

def userinputSelections(self, currentSelection, totalSelection):

    '''
    userSelectionsTotal = eval(totalSelection)
    currentSelection.text = userSelectionsTotal[2]
    '''
    

    '''
    if selectionCounter <= len(userSelectionsTotal):
        currentSelection.text = userSelectionsTotal[selectionCounter]
        selectionCounter = selectionCounter + 1
        print(selectionCounter)
    else:
        print("Make it loop back")
    '''

class HomeWindow(Screen):
    pass


class SettingsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class WashingMachineUI(App):
    def build(self):
        return


if __name__ == "__main__":
    WashingMachineUI().run()

