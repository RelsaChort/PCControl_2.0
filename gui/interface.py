from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.core.window import Window

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = "vertical"
        self.spacing = 15
        self.padding = 15

class SettingsInput(TextInput):
    def __init__(self, hint: str, **kwargs):
        super().__init__(**kwargs)
        
        self.hint_text = hint
        self.multiline = False
        self.write_tab = False
        self.hint_text_color = "#FFFFFF"
        self.background_color = "#000000"
        self.foreground_color = "#FF0000"

class SettingsField(BoxLayout):
    def __init__(self, l_text: str, textinput_text: str, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.label = MainLabel(l_text)
        self.settings_input = SettingsInput(textinput_text)
        self.add_widget(self.label)
        self.add_widget(self.settings_input)
        
    def get_value(self):
        None
    
    def set_value(self):
        None

   
class MainLabel(Label):
    def __init__(self, text:str, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = 15
        
class MainWindow(App):
    def build(self):
        scroll = ScrollView()
        layout = MainLayout()
        
        
        
        scroll.add_widget(layout)
        return scroll


MainWindow().run()