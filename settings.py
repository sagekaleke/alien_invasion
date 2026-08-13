class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's settings."""

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800

        # screen background colour
        self.bg_color = (230, 230, 230)

        # set the frames for the ship's speed
        self.ship_speed = 1.5
        self.ship_limit = 3

        # bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60,60,60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # 1 means right movement; -1 means left movement
        self.fleet_direction = 1