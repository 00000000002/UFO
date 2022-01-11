import sys
import pygame
from settings import Settings
from ship import Ship
from  bullet import Bullet
from alien1 import Alien
from time import sleep
from game_stats import GameStart
from button import Button
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.get_caption()
        self.stats = GameStart(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.bg_color = (0,0,255)
        self.play_buttton = Button(self,"play")
    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width -(2*alien_width)
        number_alien_x = available_space_x//(2*alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_width-(3*alien_height)-ship_height)
        number_rows = available_space_y//(2*alien_height)
        for row_number in range(3):
         for alien_number in range(number_alien_x):
             self._create_alien(alien_number, row_number)
    def _create_alien(self, alien_number, row_number):

            alien=Alien(self)
            alien_width, alien_height = alien.rect.size
            alien_width = alien.rect.width
            alien.x = alien_width+2*alien_width*alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
            self.aliens.add(alien)

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
             self.ship.update()
             self.bullets.update()
            if not self.aliens:
                self.bullets.empty()
                self._create_fleet()
            self._update_aliens()
            self._update_screen()
    def _check_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button( mouse_pos )

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = True
                    elif event.key == pygame.K_SPACE:
                        self._fire_bullet()
                elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT:
                            self.ship.moving_right = False
                        elif event.key == pygame.K_LEFT:
                            self.ship.moving_left = False
                        self.ship.rect.x += 1
    def _check_play_button(self,mouse_pos):
        if self.play_buttton.rect.collidepoint(mouse_pos):
            self.stats.game_active =True
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
    def _update_screen(self):
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            if not self.stats.game_active:
                self.play_buttton.draw_button()
            pygame.display.flip()
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1
    def _ship_hit(self):
     if self.stats.ships_left>0:
        self.stats.ships_left-=1
        self.stats.game_active=False
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        sleep(0.5)
     else :
        self.stats.game_active=False
        self.pygame.QUIT
if __name__ =='__main__':
    ai = AlienInvasion()
    ai.run_game()