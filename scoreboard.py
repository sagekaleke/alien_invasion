import pygame.font

class Scoreboard:
    """A class to repost scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score image
        self.prep_score()


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


    def show_score(self):
        """Draw score to the screen."""

        # show the score_image at the score_rect position
        self.screen.blit(self.score_image, self.score_rect)

