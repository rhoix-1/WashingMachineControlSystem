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

presetSetting = ["Regular", "Whites", "Colors", "Permanent_Press", "Delicates", "Custom"]
agitationSetting = ["Fast", "Slow"]
cycleSpeedSetting = ["Fast", "Slow"]
waterTempSetting = ["Warm", "Hot", "Cold"]
soakSetting = ["Yes", "No"]


class UserInterfaceApp(App):
	def build(self):
		layout = GridLayout(cols = 3)
		# Row 1
		layout.add_widget(Label(text = "Presets", font_size = "40", font_name = "Roboto/Roboto-Medium.ttf"))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 2
		layout.add_widget(Button(text = presetSetting[0], size_hint_x = None, width = 200))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 3
		layout.add_widget(Label(text = "Agitation Speed", font_size = "40", font_name = "Roboto/Roboto-Medium.ttf"))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 4
		layout.add_widget(Button(text = agitationSetting[0], size_hint_x = None, width = 150))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 5
		layout.add_widget(Label(text = "Cycle Speed", font_size = "40", font_name = "Roboto/Roboto-Medium.ttf"))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 6
		layout.add_widget(Button(text = cycleSpeedSetting[0], size_hint_x = None, width = 150))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 7
		layout.add_widget(Label(text = "Water Temp.", font_size = "40", font_name = "Roboto/Roboto-Medium.ttf"))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 8
		layout.add_widget(Button(text = waterTempSetting[0], size_hint_x = None, width = 150))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 9
		layout.add_widget(Label(text = "Include Soak", font_size = "40", font_name = "Roboto/Roboto-Medium.ttf"))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		# Row 10
		layout.add_widget(Button(text = soakSetting[0], size_hint_x = None, width = 150))
		layout.add_widget(Label(text = "1"))
		layout.add_widget(Label(text = "1"))
		return layout

if __name__ == '__main__':
    UserInterfaceApp().run()
