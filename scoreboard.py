import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to repost scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Turn the score to a rendered image."""

        # rounds the score to the nearest 10
        # -1 rounds to the nearest 10. 0 to a whole number. 1 to 1 decimal place
        # 1748.23 = 1750 (-1), 1748(0), 1748.2(1)
        rounded_score = round(self.stats.score, -1)

        # converts an int to str so it can be rendered to an image
        # pygame needs to convert a str to an image to make a use of it
        # :, is a format specifier that add a comma to the string, wherever it is needed
        score_str = f"{rounded_score:,}"

        # renders the str to an image
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # display the score at the top-right side of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):

        """Turn the high_score to a str and an image"""

        high_score = round(self.stats.high_score, -1)

        high_score_str = f"{high_score:,}"

        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """Turn the level to a str and an image"""

        level = self.stats.level
        level_str = str(level)

        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """Show how many ships are left."""

        self.ships = Group()
        
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x  = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        """Draw scores, levels, and ships to the screen."""

        # show the score_image at the score_rect position on the screen
        self.screen.blit(self.score_image, self.score_rect)

        # show the high_score_image at the top-center position on the screen
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # show the level_image at the level_rect position on the screen
        self.screen.blit(self.level_image, self.level_rect)

        # draw ships on to the screen.
        self.ships.draw(self.screen)


    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
