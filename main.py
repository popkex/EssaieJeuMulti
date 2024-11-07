# coding:utf-8

"""
TODO:
    - ajouter les collisions entre les joueurs
    - ajouter de la gravité : 
        - a reflechir mais surement une force qui va s'appliquer constament dans une direction 


    erreur l30 screen.py, supprimer les anciens murs !!!!!!!!!!
"""

import pygame
from screen import Screen
from entity import Entity
from internetManager import InternetManager
from gamePhysics import GamePhysic

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Entity(self, position=(300, 300), scale=50)
        self.internet_manager = InternetManager()
        self.game_physic = GamePhysic(self.screen)

        self.is_running = True
        self.clock = pygame.time.Clock()

    def refresh_screen(self):
        """redessine tout l'écran"""
        self.screen.window.fill(False)

        self.screen.draw_walls(self.game_physic.data_base.walls_collide)

        player_pos, all_players_pos = self.internet_manager.get_players_position()
        self.screen.draw_players(self.game_physic.data_base.walls_collide, all_players_pos)
        self.player.move()

        if not self.game_physic.debug_mode: pygame.display.flip()

    def run(self):
        """La bouche de jeu"""
        self.internet_manager.start(self)

        while self.is_running:
            self.refresh_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F6:
                        self.game_physic.debug_mode = not self.game_physic.debug_mode
                        if self.game_physic.debug_mode: print("Debug Mode Activé !") 
                        else: print("Debug Mode désactiver !")

            self.clock.tick(120)

        self.internet_manager.stop()
        pygame.quit()

game = Game()
game.run()