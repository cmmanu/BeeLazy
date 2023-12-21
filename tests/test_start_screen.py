import unittest

from kivy.clock import Clock
from kivy.uix.button import Button

from src.start_screen import StartScreen


class TestStartScreen(unittest.TestCase):
    def setUp(self):
        def mock_callback():
            pass

        self.start_screen = StartScreen(mock_callback, mock_callback, mock_callback)

    def test_set_button_width(self):
        # Add buttons to the start screen
        self.start_screen.add_widget(Button(text="Button 1"))
        self.start_screen.add_widget(Button(text="Button 2"))
        self.start_screen.add_widget(Button(text="Button 3"))

        # Call the set_button_width method
        self.start_screen.set_button_width(None)

        # Check if the button width is set correctly
        for child in self.start_screen.children:
            self.assertEqual(child.width, self.start_screen.text_width + 60)

    def test_set_button_width_smaller_text_width(self):
        # Add buttons to the start screen
        self.start_screen.add_widget(Button(text="Button 1"))
        self.start_screen.add_widget(Button(text="Button 2"))
        self.start_screen.add_widget(Button(text="Button 3"))
        self.start_screen.text_width = -5

        # Call the set_button_width method
        self.start_screen.set_button_width(None)

        # Check if the button width is set correctly
        for child in self.start_screen.children:
            self.assertEqual(child.width, self.start_screen.text_width + 60)
        self.assertEqual(self.start_screen.text_width, 0)

    def test_create_start_screen(self):
        # create_start_screen already called in setUp
        # Check if the back button is removed and the start and highscore buttons are added
        self.assertNotIn(self.start_screen.back_button, self.start_screen.children)
        self.assertIn(self.start_screen.start_button, self.start_screen.children)
        self.assertIn(self.start_screen.highscore_button, self.start_screen.children)

    def test_start_game(self):
        # Call the start_game method
        self.start_screen.start_game()

        # Add your assertions here

    def test_show_highscore(self):
        # Call the show_highscore method
        self.start_screen.show_highscore()

        # Add your assertions here


if __name__ == "__main__":
    unittest.main()
