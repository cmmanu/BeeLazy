from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore

import random


GROUND_HEIGHT = 100
"""Height of the ground from the screen bottom."""


class Player(Widget):
    """The player of the game.

    The player is the main figure in the game that needs to jump over obstacles.
    """

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.size = (50, 50)
        self.velocity = [0, 0]
        self.score = 0
        self.pos = (200, GROUND_HEIGHT)
        with self.canvas:
            self.color = Color(1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        self.velocity[1] -= 1.0  # apply gravity
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        self.rect.pos = self.pos

        # keep player on the ground
        if self.pos[1] < GROUND_HEIGHT:
            self.pos = (self.pos[0], GROUND_HEIGHT)
            self.velocity[1] = 0
        self.rect.pos = self.pos

    def jump(self):
        self.velocity[1] = 30  # set upward velocity


class Obstacle(Widget):
    """The obstacle for the player to doge.

    Obstacles will appear on the right side of the screen. The main goal for a player is to pass
    these obstacles.
    """

    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.size = (50, 50)
        self.passed_obstacles = []
        self.velocity = 5
        self.pos = (Window.width, GROUND_HEIGHT)
        with self.canvas:
            self.color = Color(1, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        self.pos = (self.pos[0] - self.velocity, GROUND_HEIGHT)
        self.rect.pos = self.pos


class Game(Widget):
    player = Player()
    obstacles = []
    theme_song = None  # Sound object for the theme song

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.score = 0
        self.highscores = []
        self.store = None
        self.score_label = Label(
            center_x=Window.width / 2, top=Window.height - 20, text="Score: 0"
        )
        self.add_widget(self.score_label)
        self.add_widget(self.player)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.bind(on_touch_down=self.on_touch_down)

    def update(self, dt):
        self.player.update()

        if len(self.obstacles) < 1:
            new_obstacle = Obstacle()
            reinforcement = (self.score / 100 ) + 1
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
            if self.player.collide_widget(obstacle):
                Clock.unschedule(self.update)
                self.score_label.text = "Game over!"
                self.theme_song.stop()
                self.save_highscores()
                self.show_restart_button()
                self.show_highscore_label()

    def on_touch_down(self, *args):
        if self.player.pos[1] == GROUND_HEIGHT:
            self.player.jump()

    def show_restart_button(self):
        restart_button = Button(
            text="Restart", size_hint=(None, None), size=(200, 100),
            pos=(Window.width / 2 - 100, Window.height / 2 - 50)
        )
        restart_button.bind(on_press=self.restart_game)  # Bind on_release event
        self.parent.add_widget(restart_button)

    def show_highscore_label(self):
        # Display highscores
        highscore_label = Label(
            center_x=Window.width / 2, top=Window.height / 1.5, text="Highscores:\n"
        )
        for i, score in enumerate(self.highscores):
            highscore_label.text += f"{i + 1}. {score}\n"
        self.add_widget(highscore_label)

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

    def load_highscores(self):
        self.store = JsonStore("highscores.json")
        if "scores" in self.store:
            self.highscores = self.store.get("scores")["scores"]
        else:
            self.highscores = []

    def save_highscores(self):
        # Update highscores
        self.highscores.append(self.score)
        self.highscores.sort(reverse=True)
        self.highscores = self.highscores[:5]  # Keep only the top 5 scores

        self.store.put("scores", scores=self.highscores)


class MyApp(App):
    def build(self):
        game = Game()
        game.theme_song = SoundLoader.load('assets/theme.mp3')  # Load the MP3 file
        if game.theme_song:
            game.theme_song.loop = True  # Set the theme song to loop
            game.theme_song.play()  # Start playing the theme song
        game.load_highscores()
        return game


if __name__ == "__main__":
    MyApp().run()
