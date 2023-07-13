import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.config import Config
from kivy.uix.image import Image
from kivy.animation import Animation

import random

from start_screen import StartScreen

GROUND_HEIGHT = 100
"""Height of the ground from the screen bottom."""

MAX_OBSTACLES = 5
"""The maximum number of obstacles in one screen."""


class Player(Widget):
    """The player of the game.

    The player is the main figure in the game that needs to jump over obstacles.
    """

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (50, 50)
        self.velocity = [0, 0]
        self.score = 0
        self.pos = (200, Window.height / 2)
        self.touched = False
        with self.canvas:
            self.color = Color(1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        if not self.touched:
            self.velocity[1] -= 0.5  # apply gravity
        new_x_pos = self.pos[0] + self.velocity[0]
        new_y_pos = self.pos[1] + self.velocity[1]
        # check if max height is reached
        if new_y_pos >= Window.height - self.size[1]:
            new_y_pos = Window.height - self.size[1]
        self.pos = (new_x_pos, new_y_pos)
        self.rect.pos = self.pos

    def fly(self):
        self.touched = True
        self.velocity[1] = 10  # set upward velocity

    def fall(self):
        self.touched = False


class Obstacle(Widget):
    """The obstacle for the player to doge.

    Obstacles will appear on the right side of the screen. The main goal for a player is to pass
    these obstacles.
    """

    sizes = [(50, 50), (50, 100), (50, 150)]

    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        self.passed_obstacles = []
        self.velocity = 5
        self.pos = (Window.width, random.randint(50, Window.height - 50))
        with self.canvas:
            self.color = Color(1, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        self.pos = (self.pos[0] - self.velocity, self.pos[1])
        self.rect.pos = self.pos


class Game(Widget):
    player = Player()
    obstacles = []
    theme_song = None

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
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
            self.bg_image = Image(
                source="assets/background.jpg", allow_stretch=True, keep_ratio=False
            )
            self.bg_image2 = Image(
                source="assets/background.jpg", allow_stretch=True, keep_ratio=False
            )
            self.bind(pos=self.update_background, size=self.update_background)

    def animate_background(self, step: int):
        anim = Animation(x=-self.bg_image.width, duration=step)
        anim.bind(on_complete=self.reset_background)
        anim.start(self.bg_image)

    def animate_background2(self, step: int):
        anim = Animation(x=-self.bg_image2.width, duration=step)
        anim.bind(on_complete=self.reset_background2)
        anim.start(self.bg_image2)

    def reset_background(self, *args):
        self.bg_image.size = self.size
        self.bg_image.pos = (Window.width, 0)
        self.animate_background(20)

    def reset_background2(self, *args):
        self.bg_image2.size = self.size
        self.bg_image2.pos = (Window.width, 0)
        self.animate_background2(20)

    def update_background(self, *args):
        self.bg_image.size = self.size
        self.bg_image2.size = self.size
        self.bg_image2.pos = (Window.width, 0)

    def start_game(self):
        self.animate_background(10)
        self.animate_background2(20)
        self.remove_widget(self.start_screen)
        self.score_label = Label(
            center_x=Window.width / 2, top=Window.height - 20, text="Score: 0"
        )
        self.add_widget(self.score_label)
        self.add_widget(self.player)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.bind(on_touch_down=self.fly)
        self.bind(on_touch_up=self.fall)
        self.load_highscores()

    def remove_start_screen(self):
        self.remove_widget(self.start_screen)

    def restart_game(self, instance):
        self.parent.remove_widget(instance)
        self.clear_widgets()
        self.player = Player()
        self.obstacles = []
        self.theme_song.play()
        self.score = 0
        self.score_label = Label(
            center_x=Window.width / 2, top=Window.height - 20, text="Score: 0"
        )
        self.add_widget(self.score_label)
        self.add_widget(self.player)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        self.player.update()
        obstacles = self.score / 30 or 1
        if obstacles > MAX_OBSTACLES:
            obstacles = MAX_OBSTACLES
        if len(self.obstacles) < obstacles:
            new_obstacle = Obstacle()
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
                self.player.pos[0] > obstacle.pos[0] + obstacle.size[0]
                and obstacle not in obstacle.passed_obstacles
            ):
                self.score += 1
                obstacle.passed_obstacles.append(obstacle)
                self.score_label.text = f"Score: {self.score}"
            if (
                self.player.collide_widget(obstacle)
                or self.player.pos[1] < -self.player.size[1]
            ):
                Clock.unschedule(self.update)
                self.score_label.text = "Game over!"
                self.theme_song.stop()
                self.save_highscores()
                self.show_restart_button()
                self.show_highscore_label()

    def fly(self, *args):
        self.player.fly()

    def fall(self, *args):
        self.player.fall()

    def show_restart_button(self):
        self.restart_button = Button(
            text="Restart",
            size_hint=(None, None),
            size=(200, 100),
            pos=(Window.width / 2 - 100, Window.height / 3),
        )
        self.restart_button.bind(on_press=self.restart_game)  # Bind on_release event
        self.parent.add_widget(self.restart_button)

    def show_highscore_label(self):
        # Display highscores
        self.highscore_label = Label(
            center_x=Window.width / 2, top=Window.height / 1.5, text="Highscores:\n"
        )
        for i, score in enumerate(self.highscores):
            self.highscore_label.text += f"{i + 1}. {score}\n"
        self.add_widget(self.highscore_label)

    def remove_highscore_label(self):
        self.remove_widget(self.highscore_label)

    def load_highscores(self):
        storage = App.get_running_app().user_data_dir
        # Create a file path within the user data directory
        file_path = os.path.join(storage, "highscores.json")
        self.store = JsonStore(file_path)

        if "scores" in self.store:
            self.highscores = self.store.get("scores")["scores"]

    def save_highscores(self):
        # Update highscores
        self.highscores.append(self.score)
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:5]  # Keep only the top 5 scores

        self.store.put("scores", scores=self.highscores)


class MyApp(App):
    def build(self):
        game = Game()
        game.theme_song = SoundLoader.load("assets/theme.mp3")  # Load the MP3 file
        if game.theme_song:
            game.theme_song.loop = True  # Set the theme song to loop
            # game.theme_song.play()  # Start playing the theme song
        game.load_highscores()
        return game


if __name__ == "__main__":
    Config.set("graphics", "orientation", "landscape")
    MyApp().run()
