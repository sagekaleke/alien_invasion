import pygame
from pygame.sprite import Sprite
# we are using sprite submodule to group related sprites together so we can act on them together.

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current location."""

        # here, super() refers to the Sprite class.
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = ai_game.settings.bullet_colour

        # create a bullet object at (0,0) and then set it to its correct position
        # The sprite’s rect stores the sprite’s position and dimensions, and Pygame often uses it as the sprite’s location on the screen.
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)

        # the bullet’s midtop point is moved to the same coordinates as the ship’s midtop point.
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""

        # Updates the position of the bullet.
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


    def draw_bullet(self):
        """Draw a bullet on the screen."""

        # draw a rectangle on the screen using this colour at this position.
        pygame.draw.rect(self.screen, self.colour, self.rect)