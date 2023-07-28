from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class StartScreen(Widget):
    """The start screen of the game.

    This screen appears before the game starts and allows the player to choose whether to start
    the game or show the highscore.
    """

    def __init__(self, start_callback, highscore_callback, back_callback, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.start_callback = start_callback
        self.highscore_callback = highscore_callback
        self.back_callback = back_callback

        self.start_button = Button(
            text="Start Game",
            size_hint=(None, None),
            size=(250, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 25),
        )
        self.start_button.bind(on_release=self.start_game)

        self.highscore_button = Button(
            text="Show Highscore",
            size_hint=(None, None),
            size=(250, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 150),
        )
        self.highscore_button.bind(on_release=self.show_highscore)

        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(250, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 150),
        )
        self.back_button.bind(on_release=self.create_start_screen)

        self.create_start_screen()

    def create_start_screen(self, *args):
        self.back_callback()
        self.remove_widget(self.back_button)
        self.add_widget(self.start_button)
        self.add_widget(self.highscore_button)

    def start_game(self, *args):
        self.start_callback()

    def show_highscore(self, *args):
        self.add_widget(self.back_button)
        self.remove_widget(self.start_button)
        self.remove_widget(self.highscore_button)
        self.highscore_callback()
