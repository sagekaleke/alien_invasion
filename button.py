import pygame.font

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initiliase the button attributes"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0) # dark green
        self.text_color = (255, 255, 255) # grey
        self.font = pygame.font.SysFont(None, 48) # None means use the default font;  48 is the font size

        # build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # the button's message needs to be prepped only once
        # Pygame works with string by rendering the text as image
        # we will do this in _prep_msg() 
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        "Turn msg into rendered image and center text on the button."

        # renders the text as an image
        # True here is used for antialising (which makes the font smoother)
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw button onto the screen."""

        # pygame.draw.rect(self.screen, self.button_color, self.rect)
        # ^ this code is also correct. it says, "draw a rectangle of this colour on the screen"

        # the below code says, "fill the rectangle with this color"
        # fill is better because we already have the rectangle as self.rect
        # we just need to fill it with a color
        # lastly, we place the text on the button

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
