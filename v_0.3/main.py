import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen



class HomeWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("kv-main.kv")

class WashingMachineUI(App):
    def build(self):
        return kv


if __name__ == "__main__":
    WashingMachineUI().run()

