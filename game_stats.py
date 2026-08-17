class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialises GameStats"""

        self.settings = ai_game.settings
        self.reset_stats()

        # high_score should never be set to 0, so we initialise it here 
        self.high_score = 0


    def reset_stats(self):
        """Initialises statistics that can change during the game."""

        self.ships_left = self.settings.ship_limit
        self.score = 0

    