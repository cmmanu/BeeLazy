"""Implements the bee with its animation."""

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.image import Image


class Bee(Image):
    """The main protoganist of the game which is a bee.

    The bee is an animated spritesheet that must not coolide with obstacles.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (260, 260)
        self.velocity = [0, 0]
        self.score = 0
        self.pos = (200, Window.height / 2)
        self.touched = False
        self.frames = []
        self.frame_idx = 0
        self.anim_delay = 0.1
        self.load_spritesheet()
        self.bind(on_texture=self.update_texture)
        Clock.schedule_interval(self.update_frame, self.anim_delay)

    def load_spritesheet(self):
        """Load spritesheet image and split it into individual frames."""

        texture = CoreImage("./assets/bee.png").texture
        cols, rows = 2, 4  # 2x4 grid of frames in the spritesheet
        frame_width, frame_height = texture.width / cols, texture.height / rows

        for row in range(rows):
            for col in range(cols):
                x_axis = col * frame_width
                # Invert y-axis to match Kivy's coordinate system
                y_axis = (rows - row - 1) * frame_height
                frame = texture.get_region(x_axis, y_axis, frame_width, frame_height)
                self.frames.append(frame)

        self.texture = self.frames[
            self.frame_idx
        ]  # Set the initial frame as the texture

    def update_frame(self, arg):
        """Update the current frame index."""

        del arg
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.texture = self.frames[self.frame_idx]

    def update_texture(self, instance, value):
        """Update the texture when it changes."""
        del instance, value
        self.texture = self.frames[self.frame_idx]

    def check_collision(self, other) -> bool:
        """Checks if the bee collided with an obstacle."""

        sprite_x, sprite_y = self.pos
        sprite_width, sprite_height = self.size
        rect_x, rect_y = other.pos
        rect_width, rect_height = other.size

        # Check for overlap of visible parts
        return (
            sprite_x < rect_x + rect_width
            and sprite_x + sprite_width - 100 > rect_x
            and sprite_y < rect_y + rect_height - 100
            and sprite_y + sprite_height - 100 > rect_y
        )

    def update(self):
        """Updates the bees position."""

        if not self.touched:
            self.velocity[1] -= 0.5  # apply gravity
        new_x_pos = self.pos[0] + self.velocity[0]
        new_y_pos = self.pos[1] + self.velocity[1]
        # check if max height is reached
        if new_y_pos >= Window.height - self.size[1] / 2:
            new_y_pos = Window.height - self.size[1] / 2
        self.pos = (new_x_pos, new_y_pos)

    def fly(self):
        """Sets the y velocity to let the bee fly."""
        self.touched = True
        self.velocity[1] = 10  # set upward velocity

    def fall(self):
        """Does not set y velocity to let the bee fall."""
        self.touched = False
