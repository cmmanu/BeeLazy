import os
import unittest
from unittest.mock import patch

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
from src.main_screen import TOP_TEXT, BeeLazy, Game, Obstacle, PowerUp
from src.obstacle import Obstacle


class TestPowerUp(unittest.TestCase):
    def setUp(self):
        self.power_up = PowerUp()

    def test_init(self):
        self.assertIsInstance(self.power_up, Widget)
        self.assertEqual(tuple(self.power_up.size), (50, 50))
        self.assertEqual(self.power_up.velocity, 7)
        self.assertGreaterEqual(self.power_up.pos[0], 0)
        self.assertLessEqual(self.power_up.pos[0], Window.width)
        self.assertGreaterEqual(self.power_up.pos[1], 50)
        self.assertLessEqual(self.power_up.pos[1], Window.height - 50)
        self.assertIsInstance(self.power_up.color, Color)
        self.assertIsInstance(self.power_up.rect, Rectangle)

    def test_update(self):
        initial_pos = self.power_up.pos
        self.power_up.update()
        self.assertEqual(self.power_up.pos[0], initial_pos[0])
        self.assertEqual(self.power_up.pos[1], initial_pos[1])
        self.assertEqual(self.power_up.rect.pos, tuple(self.power_up.pos))


class TestMainScreen(unittest.TestCase):
    def setUp(self):
        class MockThemeSong:
            def __init__(self):
                self.played = False

            def play(self):
                self.played = True

        self.game = Game()
        self.game.parent = Image()
        self.game.theme_song = MockThemeSong()

    def test_txupdate(self):
        boot_time = 0.0
        Clock.get_boottime = lambda: boot_time

        self.game.txupdate()

        expected_tex_coords = (
            -(boot_time * 0.05),
            0,
            -(boot_time * 0.05 + 1),
            0,
            -(boot_time * 0.05 + 1),
            -1,
            -(boot_time * 0.05),
            -1,
        )
        self.assertEqual(self.game.rect_1.tex_coords, expected_tex_coords)

    def test_update_background(self):
        initial_size = self.game.rect_1.size
        self.game.update_background()
        self.assertEqual(self.game.rect_1.size, initial_size)

    @patch("src.main_screen.Game.load_highscores")
    def test_start_game(self, mock_load_highscores):
        mock_load_highscores.return_value = None
        self.game.start_game()

        self.assertEqual(len(self.game.children), 2)
        self.assertNotIn(self.game.start_screen, self.game.children)
        self.assertIsInstance(self.game.score_label, Label)
        self.assertIn(self.game.score_label, self.game.children)
        self.assertIsInstance(self.game.bee, Bee)
        self.assertIn(self.game.bee, self.game.children)
        mock_load_highscores.assert_called_once()

    def test_update(self):
        self.game.bee = Bee()
        self.game.power_ups = []
        self.game.obstacles = []
        self.game.score = 0
        self.game.score_label = Label()
        self.game.game_over = False
        self.game.bee.invincible = True

        self.game.update()

        self.assertIsInstance(self.game.bee, Bee)
        self.assertGreaterEqual(len(self.game.power_ups), 0)
        self.assertGreaterEqual(len(self.game.obstacles), 0)
        self.assertGreaterEqual(self.game.score, 0)
        self.assertIsInstance(self.game.score_label, Label)
        self.assertFalse(self.game.game_over)

    def test_update_with_obstacles_and_game_over(self):
        class MockThemeSong:
            def __init__(self):
                self.played = False

            def stop(self):
                self.played = False

        class MockStore:
            def __init__(self):
                self.store = None

            def put(self, name: str, **kwargs):
                self.store = {"scores": {name: kwargs["scores"]}}

        self.game.store = MockStore()
        self.game.theme_song = MockThemeSong()
        self.game.bee = Bee()
        self.game.bee.pos = (500, -500)
        self.game.power_ups = []
        obstacle1 = Obstacle()
        obstacle1.size = (50000, 50000)
        obstacle2 = Obstacle()
        obstacle2.pos = (-500, 50)
        self.game.obstacles = [obstacle1, obstacle2]
        self.game.score = 0
        self.game.score_label = Label()
        self.game.game_over = False

        self.game.update()

        self.assertIsInstance(self.game.bee, Bee)
        self.assertGreaterEqual(len(self.game.power_ups), 0)
        self.assertGreaterEqual(len(self.game.obstacles), 0)
        self.assertGreaterEqual(self.game.score, 0)
        self.assertIsInstance(self.game.score_label, Label)
        self.assertTrue(self.game.game_over)

    def test_update_with_power_ups(self):
        self.game.bee = Bee()
        self.game.bee.size = (5000, 5000)
        power_up1 = PowerUp()
        power_up1.size = (50000, 50000)
        power_up2 = PowerUp()
        power_up2.pos = (-500, 50)
        self.game.power_ups = [power_up1, power_up2]
        self.game.obstacles = []
        self.game.score = 0
        self.game.score_label = Label()
        self.game.game_over = False

        self.game.update()

        self.assertIsInstance(self.game.bee, Bee)
        self.assertGreaterEqual(len(self.game.power_ups), 0)
        self.assertGreaterEqual(len(self.game.obstacles), 0)
        self.assertGreaterEqual(self.game.score, 0)
        self.assertIsInstance(self.game.score_label, Label)
        self.assertFalse(self.game.game_over)

    def test_update_create_powerup(self):
        self.game.bee = Bee()
        self.game.power_ups = []
        self.game.obstacles = []
        self.game.score = 0
        self.game.score_label = Label()
        self.game.game_over = False

        with patch("random.randint") as mock_randint:
            # Set the return value of randint
            mock_randint.return_value = 0
            self.game.update()

        self.assertIsInstance(self.game.bee, Bee)
        self.assertGreaterEqual(len(self.game.power_ups), 0)
        self.assertGreaterEqual(len(self.game.obstacles), 0)
        self.assertGreaterEqual(self.game.score, 0)
        self.assertIsInstance(self.game.score_label, Label)
        self.assertFalse(self.game.game_over)

    def test_timeout_function(self):
        arg = "example"
        self.game.timeout_power_up(arg)
        self.assertFalse(self.game.bee.invincible)

    def test_fly(self):
        self.game.bee = Bee()
        self.game.fly()
        self.assertTrue(self.game.bee.flying)

    def test_fall(self):
        self.game.bee = Bee()
        self.game.fall()
        self.assertFalse(self.game.bee.flying)

    def test_move(self):
        self.game.bee = Bee()

        class MockPos:
            pos: list = [100, 100]

        touch_args = (None, MockPos)
        self.game.move(*touch_args)
        self.assertTrue(self.game.bee.moving)

    def test_init_score_label(self):
        self.game.init_score_label()
        self.assertIsInstance(self.game.score_label, Label)
        self.assertEqual(self.game.score_label.center_x, Window.width / 2)
        self.assertEqual(self.game.score_label.top, TOP_TEXT)

    def test_remove_start_screen(self):
        self.game.remove_start_screen()
        self.assertNotIn(self.game.start_screen, self.game.children)

    def test_restart_game(self):
        instance = Button()
        self.game.restart_game(instance)
        self.assertFalse(self.game.game_over)
        self.assertNotIn(instance, self.game.parent.children)
        self.assertEqual(len(self.game.children), 2)
        self.assertIsInstance(self.game.bee, Bee)
        self.assertEqual(len(self.game.obstacles), 0)
        self.assertEqual(len(self.game.power_ups), 0)
        self.assertIsNotNone(self.game.theme_song)
        self.assertEqual(self.game.score, 0)
        self.assertIsInstance(self.game.score_label, Label)
        self.assertIn(self.game.score_label, self.game.children)
        self.assertIn(self.game.bee, self.game.children)
        self.assertIs(self.game.restart_button, None)

    def test_show_restart_button(self):
        self.game.show_restart_button()
        self.assertIsInstance(self.game.restart_button, Button)
        self.assertEqual(self.game.restart_button.text, "Retry")
        self.assertEqual(self.game.restart_button.size_hint, [None, None])
        self.assertEqual(self.game.restart_button.size, [200, 100])
        self.assertEqual(
            self.game.restart_button.pos,
            [Window.width / 2 - 100, Window.height / 3 - 150],
        )
        self.assertEqual(self.game.restart_button.outline_color, [0, 0, 0, 1])
        self.assertEqual(self.game.restart_button.outline_width, 2)

    def test_show_highscore_label(self):
        current_score = 10
        self.game.highscores = [5, 8, 12, 15, 20]
        self.game.show_highscore_label(current_score)
        self.assertIsInstance(self.game.highscore_label, Label)
        self.assertEqual(self.game.highscore_label.center_x, Window.width / 2)
        self.assertIn("Highscore", self.game.highscore_label.text)

    def test_show_highscore_label_with_marked_score(self):
        current_score = 10
        self.game.highscores = [5, 8, 10, 15, 20]
        self.game.show_highscore_label(current_score)
        self.assertIsInstance(self.game.highscore_label, Label)
        self.assertEqual(self.game.highscore_label.center_x, Window.width / 2)
        self.assertIn("Highscore", self.game.highscore_label.text)

    def test_remove_highscore_label(self):
        self.game.remove_highscore_label()
        self.assertNotIn(self.game.highscore_label, self.game.children)

    @patch("src.main_screen.JsonStore")
    def test_load_highscores(self, mock_jsonstore_init):
        with patch.object(App, "get_running_app") as mock_get_running_app:
            mock_user_data_dir = "/path/to/user/data/dir"
            mock_get_running_app.return_value.user_data_dir = mock_user_data_dir

            with patch.object(os.path, "join") as mock_join:
                mock_file_path = "/path/to/highscores.json"
                mock_join.return_value = mock_file_path

                mock_store = {"scores": {"scores": [10, 20, 30]}}
                mock_jsonstore_init.return_value = mock_store

                self.game.load_highscores()

                mock_get_running_app.assert_called_once()
                mock_join.assert_called_once_with(
                    mock_user_data_dir, "../highscores.json"
                )
                mock_jsonstore_init.assert_called_once_with(mock_file_path)
                self.assertEqual(self.game.highscores, mock_store["scores"]["scores"])

    def test_save_highscores(self):
        class MockStore:
            def __init__(self):
                self.store = None

            def put(self, name: str, **kwargs):
                self.store = {"scores": {name: kwargs["scores"]}}

        self.game.store = MockStore()
        self.game.save_highscores()

        expected_highscores = [0]
        self.assertEqual(self.game.highscores, expected_highscores)
        self.assertEqual(self.game.highscores[:1000], expected_highscores)


class TestBeeLazy(unittest.TestCase):
    @patch("src.main_screen.SoundLoader")
    def test_build(self, mock_soundloader):
        mock_theme_song = mock_soundloader.load.return_value
        game = BeeLazy().build()

        self.assertIsInstance(game, Game)
        self.assertEqual(game.theme_song, mock_theme_song)
        self.assertTrue(mock_theme_song.loop)
        mock_theme_song.play.assert_called_once()

    @patch("src.main_screen.SoundLoader")
    def test_build_no_theme_song(self, mock_soundloader):
        mock_soundloader.load.return_value = None
        game = BeeLazy().build()

        self.assertIsInstance(game, Game)
        self.assertIsNone(game.theme_song)


if __name__ == "__main__":
    unittest.main()
