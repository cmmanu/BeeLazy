"""This module contains the InvincibleEffect class."""
import random

from kivy.graphics import Color, Ellipse, Line
from kivy.uix.widget import Widget

from src.bee import Bee


class InvincibleEffect(Widget):
    """This class represents the invincible effect of the bee."""

    def __init__(self, bee: Bee, **kwargs):
        super().__init__(**kwargs)
        self.size = bee.size
        self.pos = (bee.pos[0] + bee.size[0] / 2, bee.pos[1] + bee.size[1] / 2)
        self.velocity = bee.velocity
        self.color = Color(1, 1, 0, 0.8)  # Yellow color with 80% opacity
        self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.glitters: list[Line] = []

    def draw_glitter(self):
        """Draws glitter around the invincible effect."""
        num_glitters = 10
        glitter_length = self.size[0] / 2

        with self.canvas:
            Color(1, 1, 0, 0.4)  # Yellow color with 80% opacity

            while len(self.glitters) > 5:
                oldest_glitter = self.glitters.pop(0)
                self.canvas.remove(oldest_glitter)

            for _ in range(num_glitters):
                glitter = Line(points=[self.pos[0], self.pos[1]])
                glitter.points += [
                    self.pos[0] + random.uniform(-glitter_length, glitter_length),
                    self.pos[1] + random.uniform(-glitter_length, glitter_length),
                ]
                glitter.width = 2
                self.glitters.append(glitter)

    def update(self, bee: Bee):
        """Updates the position of the invincible effect and glitters."""

        self.pos = (bee.pos[0] + bee.size[0] / 2, bee.pos[1] + bee.size[1] / 2)
        self.ellipse.pos = self.pos

        for glitter in self.glitters:
            glitter.points[0] = self.pos[0]
            glitter.points[1] = self.pos[1]
            glitter.points[2] += (
                self.velocity[0] / 2
            )  # Adjust the glitter's movement speed
            glitter.points[3] += (
                self.velocity[1] / 2
            )  # Adjust the glitter's movement speed
