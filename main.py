from kivy import Config

from src.main_screen import BeeLazy

if __name__ == "__main__":
    Config.set("graphics", "orientation", "landscape")
    BeeLazy().run()
