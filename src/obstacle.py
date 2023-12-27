"""Implements the Obstacle with its animation."""
import random

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.image import Image


class Obstacle(Image):
    """Implements the Obstacle with its animation."""

    def __init__(self, y: int | None = None, **kwargs):
        super().__init__(**kwargs)
        self.size = (260, 260)
        self.passed_obstacles: list[Obstacle] = []
        self.velocity = 5
        y_pos = y if y else random.randint(50, Window.height - self.size[1] / 2)
        self.pos = (Window.width, y_pos)
        self.frames: list = []
        self.frame_idx = 0
        self.anim_delay = 0.1
        self.load_spritesheet()
        self.bind(on_texture=self.update_texture)
        Clock.schedule_interval(self.update_frame, self.anim_delay)

    def load_spritesheet(self):
        """Load spritesheet image and split it into individual frames."""
        sprites = [
            {
                "texture": CoreImage("./assets/bird.png").texture,
                "cols": 6,
                "rows": 1,
                "offset": 35,
            },
            {
                "texture": CoreImage("./assets/schwalbe2.png").texture,
                "cols": 4,
                "rows": 2,
                "offset": 0,
            },
        ]

        sprite = random.choice(sprites)
        frame_width, frame_height = (
            sprite["texture"].width / sprite["cols"],
            sprite["texture"].height / sprite["rows"],
        )

        for row in range(sprite["rows"]):
            for col in range(sprite["cols"]):
                x_axis = col * frame_width
                # Invert y-axis to match Kivy's coordinate system
                y_axis = (sprite["rows"] - row - 1) * frame_height
                frame = sprite["texture"].get_region(
                    x_axis + sprite["offset"], y_axis, frame_width, frame_height
                )
                self.frames.append(frame)

        self.texture = self.frames[
            self.frame_idx
        ]  # Set the initial frame as the texture

    def update_frame(self, arg):
        """Update the current frame index of the Obstacle."""

        del arg
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.texture = self.frames[self.frame_idx]

    def update_texture(self, instance, value):
        """Update the texture of the Obstacle when it changes."""
        del instance, value
        self.texture = self.frames[self.frame_idx]

    def update(self):
        """Updates the postion of the obstacle."""
        self.pos = (self.pos[0] - self.velocity, self.pos[1])
