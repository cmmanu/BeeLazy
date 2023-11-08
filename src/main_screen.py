"""Implements classes of the main screen of the game."""

import collections
import os
import random
import typing

from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from src.bee import Bee
from src.start_screen import StartScreen

GROUND_HEIGHT = 100
"""Height of the ground from the screen bottom."""

MAX_OBSTACLES = 5
"""The maximum number of obstacles in one screen."""

TOP_TEXT = Window.height - Window.height * 0.02
"""Top text position."""


class Obstacle(Widget):
    """The obstacle for the bee to doge.

    Obstacles will appear on the right side of the screen. The main goal for the bee is to pass
    these obstacles.
    """

    sizes = [(50, 50), (50, 100), (50, 150)]

    def __init__(self, y: int | None = None, **kwargs):
        super().__init__(**kwargs)
        self.size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        self.passed_obstacles: list[Obstacle] = []
        self.velocity = 5
        y_pos = y if y else random.randint(50, Window.height - 50)
        self.pos = (Window.width, y_pos)
        with self.canvas:
            self.color = Color(1, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        """Updates the postion of the obstacle."""
        self.pos = (self.pos[0] - self.velocity, self.pos[1])
        self.rect.pos = self.pos


class PowerUp(Widget):
    """The PowerUp for the bee to gain.

    PowerUps will appear on the right side of the screen. The main goal for the bee is to gain
    those PowerUps to reach an invincible state for a bit of a time.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)
        self.velocity = 7
        self.pos = (Window.width, random.randint(50, Window.height - 50))
        with self.canvas:
            self.color = Color(1, 1, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        """Updates the postion of the PowerUp."""
        self.pos = (self.pos[0] - self.velocity, self.pos[1])
        self.rect.pos = self.pos


class Game(Widget):
    """
    The main game object where its methods uses obstacles and the bee and updates them
    periodically.
    """

    bee = Bee()
    obstacles: list[Obstacle] = []
    power_ups: list[PowerUp] = []
    theme_song = None
    last_positions: typing.Deque = collections.deque(maxlen=5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.highscores = []
        self.store = None
        self.score_label = None
        self.highscore_label = None
        self.restart_button = None
        self.start_screen = StartScreen(
            start_callback=self.start_game,
            highscore_callback=self.show_highscore_label,
            back_callback=self.remove_highscore_label,
        )
        self.add_widget(self.start_screen)
        with self.canvas.before:
            self.img = Image(
                source="assets/background2.jpg", allow_stretch=True, keep_ratio=False
            )
            self.texture = self.img.texture
            self.texture.wrap = "repeat"
            self.rect_1 = Rectangle(texture=self.texture, size=self.size, pos=self.pos)
            self.bind(pos=self.update_background, size=self.update_background)

    def txupdate(self, *args):
        """Updates the background position."""

        del args
        boot_time = Clock.get_boottime()
        self.rect_1.tex_coords = (
            -(boot_time * 0.05),
            0,
            -(boot_time * 0.05 + 1),
            0,
            -(boot_time * 0.05 + 1),
            -1,
            -(boot_time * 0.05),
            -1,
        )

    def update_background(self, *args):
        """Updates the size of the background after initial creation."""

        del args
        self.rect_1.size = self.size

    def start_game(self):
        """
        Method to call to start the game.

        Adds all relevant widgets. Initially there is the possibility to start the game or the show
        the highscore.
        """

        Clock.schedule_interval(self.txupdate, 0)
        self.remove_widget(self.start_screen)
        self.init_score_label()
        self.add_widget(self.score_label)
        self.add_widget(self.bee)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.bind(on_touch_down=self.fly)
        self.bind(on_touch_up=self.fall)
        self.bind(on_touch_move=self.move)
        self.load_highscores()

    def init_score_label(self):
        """Initializes the score label with its postion and text."""

        self.score_label = Label(
            center_x=Window.width / 2, top=TOP_TEXT, text="Score: 0"
        )

    def remove_start_screen(self):
        """Removes the start screen as widget."""

        self.remove_widget(self.start_screen)

    def restart_game(self, instance):
        """Restarts the game by clearing and resetting everything."""

        self.parent.remove_widget(instance)
        self.clear_widgets()
        self.bee = Bee()
        self.obstacles = []
        self.power_ups = []
        self.theme_song.play()
        self.score = 0
        self.init_score_label()
        self.add_widget(self.score_label)
        self.add_widget(self.bee)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.txupdate, 0)

    def update(self, *args):
        """
        Updates the game by updating the bee and obstacles.

        Adds obstacles to the screen and also updates the score.
        """

        del args
        self.bee.update()

        # small change for a power up to pop up on the screen
        if random.randint(0, 1400) == 0 and len(self.power_ups) < 1:
            new_powerup = PowerUp()
            self.power_ups.append(new_powerup)
            self.add_widget(new_powerup)

        for power_up in self.power_ups:
            power_up.update()
            if power_up.pos[0] < -power_up.size[0]:
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)
            # include invincible state for bee for 4s

        self.last_positions.append(self.bee.pos[1])

        if all(
            pos == self.last_positions[0] or abs(self.last_positions[0] - pos) <= 5
            for pos in self.last_positions
        ):
            y_pos = self.bee.pos[1]
        else:
            y_pos = None

        obstacles = self.score / 30 or 1
        obstacles = min(obstacles, MAX_OBSTACLES)
        if len(self.obstacles) < obstacles:
            new_obstacle = Obstacle(y_pos)
            reinforcement = (self.score / 100) + 1
            new_obstacle.velocity = reinforcement * random.randint(10, 20)
            self.obstacles.append(new_obstacle)
            self.add_widget(self.obstacles[-1])

        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.pos[0] < -obstacle.size[0]:
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
            if (
                self.bee.pos[0] > obstacle.pos[0] + obstacle.size[0]
                and obstacle not in obstacle.passed_obstacles
            ):
                self.score += 1
                obstacle.passed_obstacles.append(obstacle)
                self.score_label.text = f"Score: {self.score}"
            if (
                self.bee.check_collision(obstacle)
                or self.bee.pos[1] < -self.bee.size[1]
            ):
                Clock.unschedule(self.update)
                Clock.unschedule(self.txupdate)
                self.remove_widget(self.bee)
                self.score_label.text = "Game over!"
                self.theme_song.stop()
                self.save_highscores()
                self.show_restart_button()
                self.show_highscore_label(self.score)

    def fly(self, *args):
        """Activates flying mode for the bee."""

        del args
        self.bee.fly()

    def fall(self, *args):
        """Activates fall mode for the bee."""

        del args
        self.bee.fall()

    def move(self, *args):
        """Activates move mode for the bee."""
        self.bee.move(args)

    def show_restart_button(self):
        """Adds the restart button after a game over."""

        self.restart_button = Button(
            text="Retry",
            size_hint=(None, None),
            size=(200, 100),
            pos=(Window.width / 2 - 100, Window.height / 3 - 150),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.restart_button.bind(on_press=self.restart_game)  # Bind on_release event
        self.parent.add_widget(self.restart_button)

    def show_highscore_label(self, current_score: int | None = None):
        """Adds the highscore label in game."""

        # Display highscores
        self.highscore_label = Label(
            center_x=Window.width / 2,
            text="Highscores:\n",
            color=(1, 1, 1, 1),
            font_size="24sp",
            outline_color=(0, 0, 0, 1),
            outline_width=3,
            markup=True,
        )

        highscore_marked = False
        for i, score in enumerate(self.highscores):
            if score == current_score and not highscore_marked:
                self.highscore_label.text += (
                    f"[color=#FFFF00]      {i + 1}. {score}[/color]\n"
                )
                highscore_marked = True
                continue
            if i < 5:
                self.highscore_label.text += f"      {i + 1}. {score}\n"

        offset = self.score_label.size[1] if self.score_label else 0
        self.highscore_label.top = TOP_TEXT - 3 * self.highscore_label.size[1] - offset
        self.add_widget(self.highscore_label)

    def remove_highscore_label(self):
        """Removes the highscore label when gaming over."""

        self.remove_widget(self.highscore_label)

    def load_highscores(self):
        """Loads the high score when opening the game."""

        storage = App.get_running_app().user_data_dir
        # Create a file path within the user data directory
        file_path = os.path.join(storage, "../highscores.json")
        self.store = JsonStore(file_path)

        if "scores" in self.store:
            self.highscores = self.store.get("scores")["scores"]

    def save_highscores(self):
        """Saves the highscore in the store."""

        # Update highscores
        self.highscores.append(self.score)
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:1000]  # Keep only the top 100 scores

        self.store.put("scores", scores=self.highscores)


class BeeLazy(App):
    """Class that builds the game and starts the theme song."""

    def build(self):
        game = Game()
        game.theme_song = SoundLoader.load("assets/theme.mp3")  # Load the MP3 file
        if game.theme_song:
            game.theme_song.loop = True  # Set the theme song to loop
            game.theme_song.play()  # Start playing the theme song
        game.load_highscores()
        return game
