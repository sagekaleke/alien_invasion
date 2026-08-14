class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's settings."""

        # screen settings
        # while our program allows the screen to set the game to the native resolution of the screen we are working on, 
        # this is still needed because we need it to set screen-size-related conditions in our program
        # pygame.display.set_mode((0, 0), pygame.FULLSCREEN) later changes these values to match the screen resolution we are playing on        
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