import unittest

from kivy.graphics import Ellipse, Line
from kivy.uix.widget import Widget

from src.bee import Bee
from src.invincible_effect import InvincibleEffect


class TestInvincibleEffect(unittest.TestCase):
    def setUp(self):
        self.bee = Bee()
        self.invincible_effect = InvincibleEffect(self.bee)

    def test_init(self):
        self.assertIsInstance(self.invincible_effect, Widget)
        self.assertEqual(self.invincible_effect.size, self.bee.size)
        self.assertEqual(
            tuple(self.invincible_effect.pos),
            (
                self.bee.pos[0] + self.bee.size[0] / 2,
                self.bee.pos[1] + self.bee.size[1] / 2,
            ),
        )
        self.assertEqual(self.invincible_effect.velocity, self.bee.velocity)
        self.assertIsInstance(self.invincible_effect.ellipse, Ellipse)
        self.assertEqual(self.invincible_effect.glitters, [])

    def test_update_no_glitter(self):
        self.invincible_effect.update(self.bee)
        self.assertEqual(
            tuple(self.invincible_effect.pos),
            (
                self.bee.pos[0] + self.bee.size[0] / 2,
                self.bee.pos[1] + self.bee.size[1] / 2,
            ),
        )
        self.assertEqual(
            self.invincible_effect.ellipse.pos, tuple(self.invincible_effect.pos)
        )

    def test_update_with_glitter(self):
        self.invincible_effect.draw_glitter()
        self.invincible_effect.update(self.bee)
        self.assertEqual(
            tuple(self.invincible_effect.pos),
            (
                self.bee.pos[0] + self.bee.size[0] / 2,
                self.bee.pos[1] + self.bee.size[1] / 2,
            ),
        )
        self.assertEqual(
            self.invincible_effect.ellipse.pos, tuple(self.invincible_effect.pos)
        )

    def test_draw_glitter(self):
        self.invincible_effect.draw_glitter()
        # call second time to test removing oldest glitter
        self.invincible_effect.draw_glitter()
        self.assertEqual(len(self.invincible_effect.glitters), 15)
        for glitter in self.invincible_effect.glitters:
            self.assertIsInstance(glitter, Line)
            self.assertEqual(glitter.width, 2)
            self.assertEqual(len(glitter.points), 4)
            self.assertGreaterEqual(
                glitter.points[0],
                self.invincible_effect.pos[0] - self.invincible_effect.size[0] / 2,
            )
            self.assertLessEqual(
                glitter.points[0],
                self.invincible_effect.pos[0] + self.invincible_effect.size[0] / 2,
            )
            self.assertGreaterEqual(
                glitter.points[1],
                self.invincible_effect.pos[1] - self.invincible_effect.size[0] / 2,
            )
            self.assertLessEqual(
                glitter.points[1],
                self.invincible_effect.pos[1] + self.invincible_effect.size[0] / 2,
            )
            self.assertGreaterEqual(
                glitter.points[2],
                self.invincible_effect.pos[0] - self.invincible_effect.size[0] / 2,
            )
            self.assertLessEqual(
                glitter.points[2],
                self.invincible_effect.pos[0] + self.invincible_effect.size[0] / 2,
            )
            self.assertGreaterEqual(
                glitter.points[3],
                self.invincible_effect.pos[1] - self.invincible_effect.size[0] / 2,
            )
            self.assertLessEqual(
                glitter.points[3],
                self.invincible_effect.pos[1] + self.invincible_effect.size[0] / 2,
            )


if __name__ == "__main__":
    unittest.main()
