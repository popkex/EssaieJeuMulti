# coding:utf-8

"""
TODO:
    - ajouter les collisions entre les joueurs
    - ajouter de la gravité : 
        - a reflechir mais surement une force qui va s'appliquer constament dans une direction 
"""

"""
TODO ERREUR:
    - l'activation/desactivation de la dedection des collisions avec les murs n'est pas bien:
        - vérifier a partir de la moitier de la hauteur/largeur ?
"""

import pygame
from screen import Screen
from entity import Entity
from internetManager import InternetManager
from gamePhysics import GamePhysic

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen(self)
        self.player = Entity(self, position=(100, 0), scale=50)
        self.internet_manager = InternetManager()
        self.game_physic = GamePhysic(self.screen, self)

        self.is_running = True
        self.key_pressed = []
        self.clock = pygame.time.Clock()

    def refresh_screen(self):
        """redessine tout l'écran avec la caméra"""
        player_pos, all_players_pos = self.internet_manager.get_players_position()
        self.screen.refresh_screen(player_pos, all_players_pos)
        self.player.move()

    def run(self):
        """La bouche de jeu"""
        self.internet_manager.start(self)

        while self.is_running:
            self.refresh_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    self.key_pressed.append(event.key)

                    if event.key == pygame.K_F6:
                        self.game_physic.debug_mode = not self.game_physic.debug_mode
                        if self.game_physic.debug_mode: print("Debug Mode Activé !") 
                        else: print("Debug Mode désactiver !")

                if event.type == pygame.KEYUP:
                    self.key_pressed.remove(event.key)

            self.clock.tick(60)

        self.internet_manager.stop()
        pygame.quit()

game = Game()
game.run()