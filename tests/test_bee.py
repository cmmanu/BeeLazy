import unittest

from kivy.graphics.texture import TextureRegion

from src.bee import Bee


class TestBee(unittest.TestCase):
    def setUp(self):
        self.bee = Bee()

    def test_load_spritesheet(self):
        # Call the load_spritesheet method
        self.bee.load_spritesheet()

        # Check if the frames list is populated correctly
        self.assertEqual(len(self.bee.frames), 16)
        self.assertIsInstance(self.bee.frames[0], TextureRegion)

    def test_update_frame(self):
        # Set the initial frame index
        self.bee.frame_idx = 0

        # Call the update_frame method
        self.bee.update_frame(None)

        # Check if the frame index is updated correctly
        self.assertEqual(self.bee.frame_idx, 1)

    def test_update_texture(self):
        # Set the initial frame index
        self.bee.frame_idx = 0

        # Call the update_texture method
        self.bee.update_texture(None, None)

        # Check if the texture is updated correctly
        self.assertIsInstance(self.bee.texture, TextureRegion)
        self.assertEqual(self.bee.texture, self.bee.frames[0])

    def test_check_collision(self):
        # Create a mock obstacle
        class MockObstacle:
            def __init__(self):
                self.pos = (100, 100)
                self.size = (300, 300)

        # Set the bee's position and size
        self.bee.pos = (150, 150)
        self.bee.size = (50, 50)

        # Call the check_collision method with the mock obstacle
        result = self.bee.check_collision(MockObstacle())

        # Check if the collision is detected correctly
        self.assertTrue(result)

    def test_update(self):
        # Set the bee's initial position and velocity
        self.bee.pos = (-5000, 200)
        self.bee.velocity = [0, 0]

        # Call the update method
        self.bee.update()

        # Check if the bee's position is updated correctly
        self.assertEqual(self.bee.pos, [-130.0, 199.5])

    def test_update_flying(self):
        # Set the bee's initial position and velocity
        self.bee.pos = (200, 5000)
        self.bee.flying = True
        self.bee.velocity = [0, 0]

        # Call the update method
        self.bee.update()

        # Check if the bee's position is updated correctly
        self.assertEqual(self.bee.pos[0], 200)

    def test_update_moving(self):
        # Set the bee's initial position and velocity
        self.bee.pos = (5000, 5000)
        self.bee.moving = True
        self.bee.velocity = [0, 0]

        # Call the update method
        self.bee.update()

        # Check if the bee's position is updated correctly
        self.assertLess(self.bee.pos[1], 5000)

    def test_fly(self):
        # Call the fly method
        self.bee.fly()

        # Check if the flying attribute is set to True
        self.assertTrue(self.bee.flying)

    def test_fall(self):
        # Set the bee's initial attributes
        self.bee.flying = True
        self.bee.moving = True
        self.bee.old_move_pos = (100, 100)

        # Call the fall method
        self.bee.fall()

        # Check if the flying, moving, and old_move_pos attributes are updated correctly
        self.assertFalse(self.bee.flying)
        self.assertFalse(self.bee.moving)
        self.assertIsNone(self.bee.old_move_pos)

    def test_move(self):
        # Set the bee's initial attributes
        self.bee.moving = False
        self.bee.old_move_pos = None

        class MockPos:
            pos: list = [100, 100]

        # Call the move method with mock arguments
        self.bee.move([None, MockPos])

        # Check if the moving and old_move_pos attributes are updated correctly
        self.assertTrue(self.bee.moving)
        self.assertIsNotNone(self.bee.old_move_pos)


if __name__ == "__main__":
    unittest.main()
