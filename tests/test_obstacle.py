import unittest

from kivy.core.window import Window
from kivy.graphics.texture import TextureRegion
from kivy.uix.image import Image

from src.obstacle import Obstacle


class TestObstacle(unittest.TestCase):
    def setUp(self):
        self.obstacle = Obstacle()

    def test_load_spritesheet(self):
        # Call the load_spritesheet method
        self.obstacle.load_spritesheet()

        # Check if the frames list is populated correctly
        self.assertEqual(len(self.obstacle.frames), 12)
        self.assertIsInstance(self.obstacle.frames[0], TextureRegion)

    def test_update_frame(self):
        # Set the initial frame index
        self.obstacle.frame_idx = 0

        # Call the update_frame method
        self.obstacle.update_frame(None)

        # Check if the frame index is updated correctly
        self.assertEqual(self.obstacle.frame_idx, 1)

    def test_update_texture(self):
        # Set the initial frame index
        self.obstacle.frame_idx = 0

        # Call the update_texture method
        self.obstacle.update_texture(None, None)

        # Check if the texture is updated correctly
        self.assertIsInstance(self.obstacle.texture, TextureRegion)
        self.assertEqual(self.obstacle.texture, self.obstacle.frames[0])


if __name__ == "__main__":
    unittest.main()
