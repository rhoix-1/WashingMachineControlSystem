# Platt Tech Nasa Hunch Team (Josepher Shunaula & Ethan Feldman)
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

'''
import dataCollector
dataCollector.SendData()
'''

class HomeScreen(GridLayout):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.cols = 3
        # Row 1
        self.add_widget(Label(text = "Presets", font_size="50"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 2
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 3
        self.add_widget(Label(text = "Agitation Speed", font_size="30"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 4
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 5
        self.add_widget(Label(text = "Cycle Speed", font_size="30"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 6
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 7
        self.add_widget(Label(text = "Water Temp.", font_size="30"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 8
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 9
        self.add_widget(Label(text = "Include Soak", font_size="30"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        # Row 10
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))
        self.add_widget(Label(text = "1"))

class UserInterfaceApp(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    UserInterfaceApp().run()