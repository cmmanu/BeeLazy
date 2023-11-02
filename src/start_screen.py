"""Implements classes of the start screen of the game."""
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class StartScreen(Widget):
    """The start screen of the game.

    This screen appears before the game starts and allows the player to choose whether to start
    the game or show the highscore.
    """

    text_width: int = 0

    def __init__(self, start_callback, highscore_callback, back_callback, **kwargs):
        super().__init__(**kwargs)
        self.start_callback = start_callback
        self.highscore_callback = highscore_callback
        self.back_callback = back_callback

        self.start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(250, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 25),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.start_button.bind(on_release=self.start_game)

        self.highscore_button = Button(
            text="Highscores",
            size_hint=(None, None),
            size=(250, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 150),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.highscore_button.bind(on_release=self.show_highscore)

        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(250, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 150),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.back_button.bind(on_release=self.create_start_screen)

        self.create_start_screen()

        # update the button width in respect to its text after rendering
        Clock.schedule_once(self.set_button_width, 0)

    def set_button_width(self, args):
        """Sets the button width to its text width.

        Always takes the largest text from all buttons."""
        del args
        for child in self.children:
            max_width = max(c.texture_size[0] for c in self.children)
            if max_width > self.text_width:
                self.text_width = max_width
            child.size_hint_x = None
            child.width = self.text_width + 60

    def create_start_screen(self, *args):
        """Creates the start screen on start up."""

        del args
        self.back_callback()
        self.remove_widget(self.back_button)
        self.add_widget(self.start_button)
        self.add_widget(self.highscore_button)

    def start_game(self, *args):
        """Triggers the main screen by starting the game."""

        del args
        self.start_callback()

    def show_highscore(self, *args):
        """Shows the highscore on the start screen."""

        del args
        self.add_widget(self.back_button)
        self.remove_widget(self.start_button)
        self.remove_widget(self.highscore_button)
        self.highscore_callback()

        # update the button width in respect to its text after rendering
        Clock.schedule_once(self.set_button_width, 0)
