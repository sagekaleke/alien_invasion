import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """ Intitialise the ship and set its starting position."""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a float for the ship's exact horizontal position
        # this variable is created so we can work with speeds in decimals
        self.x = float(self.rect.x)

        # movement flag; starts with the ship that's not moving
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        """Draw the ship at the location specified by self.rect object"""
    
        self.screen.blit(self.image, self.rect)


    def update(self):
        """Update the ship's position based on the keys pressed"""

        # update self.x, not self.rect.x
        # .right/.left attributes return the x-coordinates of the ship and the screen's rects
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x 

    def center_ship(self):
        """Center the ship on the screen."""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
