from kivy import Config

from src.main_screen import MyApp

if __name__ == "__main__":
    Config.set("graphics", "orientation", "landscape")
    MyApp().run()
