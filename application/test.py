import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout

class MyApp(App):
    def build(self):
        layout = FloatLayout()
        label = Label(
            text='test',
            pos=(20, 20),
            size=(180, 100),
            size_hint=(None, None))
        with label.canvas:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=label.pos, size=label.size)

        layout.add_widget(label)

        return layout


if __name__ == '__main__':
    MyApp().run()
