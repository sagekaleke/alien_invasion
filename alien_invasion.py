import sys, pygame

from time import sleep

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    # init() is a constructor method that sets up the initial state i.e.the attributes of any new object made using this class
    def __init__(self):
        """Initialise the game, and create game resources."""

        # sets up all of Pygame's internal modules (display, font, mixer, etc.) before they can be used
        pygame.init()

        # create an instance of Clock class to keep track of the frame rate and time elasped. 
        # it doesn't provide literal date and time
        self.clock = pygame.time.Clock()
        # create an instance of the Settings class
        self.settings = Settings()

        # shows the display screen and by 'mode', we mean the configuration of the screen
        # pygame is a module, .display is its submodule, .set_mode is .display's ()
        # 0,0 sets the display in accordance to the native resolution of the display
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # fetch and store the fullscreen display's width and height in the Settings object
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # sets the caption/title of the game
        pygame.display.set_caption("Alien Invasion")

        # create an instance of GameStats from the GameStats class to store the gamestats and pass the current AlienInvasion instance to it
        self.stats = GameStats(self)

        # create an instance of a ship from the Ship class and pass the current AlienInvasion instance to it
        self.ship = Ship(self)

        # create a group to list all the bullets
        self.bullets = pygame.sprite.Group()

        # create an instance of an alien from the Alien class
        self.aliens = pygame.sprite.Group()

        # create a fleet of aliens
        # this is not added to run_game() because a fleet needs to be created only once
        self._create_fleet()

        # start alien invasion in an active state
        self.game_active = False

        # make the play button
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            # the parts of the game that should run only when the game is active
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)  # limit the game loop to a maximum of 60 FPS by pausing the loop as necessary


    def _check_events(self):
        """Watch for keyboard and mouse events"""

        # the _ indicates a helper function, which is used to refactor the code in run_game
        # this helper function checks for events
        # an event is any activity a user does using the input devices.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit refers to the window-close button
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start new game when the player clicks play"""

        # collidepoint() checks whether the point of the mouse click overlaps the region defined by the Play button’s rect
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        # we want the click to be registered only when the game is active
        if button_clicked and not self.game_active:

            # reset the game's level
            self.settings.intitialize_dynamic_settings()

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

            # reset the game stats
            self.stats.reset_stats()
            self.game_active = True

            # empty the bullets and the aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            


    def _check_keydown_events(self, event):
        """Respond to keypresses"""

        # start moving the ship right
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullets()


    def _check_keyup_events(self, event):
        """Respond to keyups"""

        # stop the right movement of the ship
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullets(self):
        """Create a new bullet and add it to the bullets group."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Updates the positions of the bullets and delete old bullets"""

        # move the bullet upwards
        # update() automatically calls update() for each sprite in a group   
        # it runs once each time _update_bullets is called 
        self.bullets.update()

        # get rid of the bullets that have disappeared
        # we use copy() so we can loop over all the bullets in self.bullets,
        # while the original bullets keep dissappearing
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


        self._check_bullet_alien_collisions()


    def _update_screen(self):
        """Build a screen and keep it updated."""

        # redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # draw bullets, one at a time
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # blit/draw/copy the ship on the screen at its current location.
        self.ship.blitme()

        # draw all the aliens in the group onto the screen
        self.aliens.draw(self.screen)  

        # draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # while the user sees one screen, another is being created in the background.
        # .flip() flips (brings forth) the screen at the back to the front.
        pygame.display.flip()


    def _create_fleet(self):
        """ Create a fleet of aliens."""

        # create an alien and keep creating them until there's no space left.
        # the space between aliens is one alien width and height
    
        # self here is not being passed in the place of Sprite in alien.py
        # it is being passed to __init__(self, ai_game)
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        # multiplied by 10 to leave space for the last alien and the ship
        while current_y < (self.settings.screen_height - 10 * alien_height):
            # multiplied by 2 to leave space for the last alien and some emptiness
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # finished a row; 
            # reset x value so the new row starts at the left of the screen
            # increment y value such that there is an empty space equal to one alien between two aliens on the y axis
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
            """Create an alien and set its position on the screen"""
            
            new_alien = Alien(self)

            # we created a differnt variable so the values of new_alien.x are precise
            # we need new_alien.x as a different variable because new_alien.rect.x cannot store a float
            # new_alien.x keeps track of the precise wvalue of the x
            new_alien.x = x_position # this line is not being used meaningfully as of now
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)


    def _update_aliens(self):
        """Update the movement of all the aliens in the fleet."""

        # check if an alien has hit an edge
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collisions
        # Group vs Group → groupcollide()  
        # One Sprite vs Group → spritecollideany()
        # returns the first alien that has collided with the ship
        # otherwise, returns None
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """Respond appropriately if any alien has reached an edge."""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop and change the fleet direction of the aliens hitting the edge."""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_bullet_alien_collisions(self):
        """To check for any bullets that have hit aliens."""
        
        # if so get rid of the alien
        # this returns a dictionary with bullets as keys, and aliens as values
        # False means that bullets won't be deleted upon collission and vice-verse 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        # check if the fleet is destroyed
        if not self.aliens:
            # remove existing bullets
            # the reason empty() isn't taking self.bullets as an argument is 
            # because self.bullets is an object and .epmty() is a method associated to it
            self.bullets.empty()
            # create a new fleet
            self._create_fleet()
            # increase the speeds if every alien is shot down
            self.settings.increase_speed()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:

            # decrease the number of ships
            self.stats.ships_left -= 1

            # remove all the bullets and remaining aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and center thee ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)

        else:
            self.game_active = False
            # make the cursor visible
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # treat it the same as a ship getting hit
                self._ship_hit()
                break


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()