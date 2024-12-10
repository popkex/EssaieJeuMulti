# coding:utf-8

"""
TODO:
    - faire le placement des buildings quand click gauche est appuyer
"""

import pygame
from systems import building as _build
from src.screen import Screen
from src.entity import Entity
from src.internetManager import InternetManager
from src.gamePhysics import GamePhysic

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen(self)
        self.player = Entity(self, position=(100, 0), scale=50)
        self.internet_manager = InternetManager()
        self.game_physic = GamePhysic(self.screen, self)

        self.building = _build
        self.building.buildings = _build.Building(self)
        self.building = self.building.buildings

        self.is_running = True
        self.key_pressed = []
        self.place_building = False
        self.clock = pygame.time.Clock()

    def refresh_screen(self, is_online=True):
        """redessine tout l'écran avec la caméra"""
        player_pos, all_players_pos = self.internet_manager.get_players_position()
        self.screen.refresh_screen(player_pos, all_players_pos, is_online=is_online)
        self.player.move()

    def update_game(self):
        if self.place_building:
            self.building.start_place(self.place_building.data.img) 
        else:
            self.building.reset_place()

    def run(self):
        """La bouche de jeu"""
        self.internet_manager.start(self)
        self.drill = _build.Drill((16, 16))

        while self.is_running:
            self.update_game()
            self.refresh_screen(is_online=self.internet_manager.get_online_mode())
            pygame.display.flip()

            self.building.update_all_building()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    self.key_pressed.append(event.key)

                    if event.key == pygame.K_1:
                        if self.place_building: self.place_building = None
                        else: self.place_building = _build.Drill(is_init=False)


                    if event.key == pygame.K_F6:
                        self.game_physic.debug_mode = not self.game_physic.debug_mode
                        if self.game_physic.debug_mode: print("Debug Mode Activé !") 
                        else: print("Debug Mode désactiver !")

                    if event.key == pygame.K_F7:
                        self.internet_manager.switch_online_mode()

                if event.type == pygame.KEYUP:
                    self.key_pressed.remove(event.key)

            self.clock.tick(60)

        self.internet_manager.stop()
        pygame.quit()

game = Game()
game.run() 