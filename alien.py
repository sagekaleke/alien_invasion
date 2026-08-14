import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien."""

    def __init__(self, ai_game):
        """Initialises the alien and sets its position on the screen."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the alien image and set its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # start each alien near the top-left corner
        # we have set their x and y axises based on their width and height
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if an alien has hit an edge"""

        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move alien to the right or left"""

        # if the direction is left, -1 will be multiplied, else 1
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x