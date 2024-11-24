# coding:utf-8

"""
TODO:
    - faire le nouveau systeme de position (par case de x par x)
    - faire le systeme qui permet a la foreuse de miner (juste a update pour toute les foreuses)
    - faire une liste de toute les foreuse
    - modifier la facon dont les foreuses sont afficher (dans le screen l35)
    - faire en sorte qu'on puisse ajouter ou supprimer les foreuses
    - envoyer au server si une foreuse est envoyer ou supprimer
    - faire en sorte qu'on puisse mettre des foreuses a certains endroit
    - faire une sortie pour les convoyeurs 
    - faire les convoyeurs
    - ... ect quoi
"""

import pygame
from systems import building 
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
        self.building = building

        self.building.buildings = building.Building(self)

        self.is_running = True
        self.key_pressed = []
        self.clock = pygame.time.Clock()

    def refresh_screen(self):
        """redessine tout l'écran avec la caméra"""
        player_pos, all_players_pos = self.internet_manager.get_players_position()
        self.screen.refresh_screen(player_pos, all_players_pos, self.drill.data)
        self.player.move()

    def run(self):
        """La bouche de jeu"""
        self.internet_manager.start(self)
        self.drill = building.Drill((300, 200))

        while self.is_running:
            self.refresh_screen()
            pygame.display.flip()

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