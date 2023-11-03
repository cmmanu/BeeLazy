"""Implements the bee with its animation."""
import collections
import typing

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.image import Image

HITBOX_OFFSET = 85


class Bee(Image):
    """The main protoganist of the game which is a bee.

    The bee is an animated spritesheet that must not coolide with obstacles.
    """

    old_move_pos = None
    last_positions: typing.Deque = collections.deque(maxlen=10)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (260, 260)
        self.velocity = [0, 0]
        self.score = 0
        self.pos = (200, Window.height / 2)
        self.flying = False
        self.moving = False
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
            and sprite_x + sprite_width - HITBOX_OFFSET > rect_x
            and sprite_y < rect_y + rect_height - HITBOX_OFFSET
            and sprite_y + sprite_height - HITBOX_OFFSET > rect_y
        )

    def update(self):
        """Updates the bees position."""

        if self.flying:
            self.velocity[1] = 10  # set upward velocity
        if self.moving:
            self.velocity[1] = 0  # moving to the right or left
        else:
            self.velocity[1] -= 0.5  # apply gravity

        self.last_positions.append(self.pos[1])
        # when the y position stays the same we will fall
        if all(pos == self.last_positions[0] for pos in self.last_positions):
            self.fall()

        new_x_pos = self.pos[0] + self.velocity[0]
        new_y_pos = self.pos[1] + self.velocity[1]

        # check if bee exceeds screen
        if new_y_pos >= Window.height - self.size[1] / 2:
            new_y_pos = Window.height - self.size[1] / 2
        if new_x_pos >= Window.width - self.size[0] / 2:
            new_x_pos = Window.width - self.size[0] / 2
        if new_x_pos <= 0 - self.size[0] / 2:
            new_x_pos = 0 - self.size[0] / 2

        self.pos = (new_x_pos, new_y_pos)

    def fly(self):
        """Sets the y velocity to let the bee fly."""
        self.flying = True

    def fall(self):
        """Does not set y velocity to let the bee fall."""
        self.flying = False
        self.moving = False
        self.old_move_pos = None

    def move(self, *args):
        """Update bee's X-coordinate based on touch movement."""
        self.moving = True
        if not self.old_move_pos:
            self.old_move_pos = args[0][1].pos[0]
        offset = args[0][1].pos[0] - self.old_move_pos
        self.old_move_pos = args[0][1].pos[0]
        self.pos = (self.pos[0] + offset, self.pos[1])
