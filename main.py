import pygame
from screen import Screen
from entity import Entity
from internetManager import InternetManager
from gamePhysics import GamePhysic

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Entity(self, position=(300, 300), scale=15)
        self.internet_manager = InternetManager()
        self.game_physic = GamePhysic()

        self.is_running = True
        self.clock = pygame.time.Clock()

    def refresh_screen(self):
        """redessine tout l'écran"""
        self.screen.window.fill(False)

        self.screen.draw_walls(self.game_physic.data_base.walls_collide)

        player_pos, all_players_pos = self.internet_manager.get_players_position()
        self.player.move()
        self.screen.draw_players(all_players_pos)

        pygame.display.flip()

    def run(self):
        """La bouche de jeu"""
        self.internet_manager.start(self)

        while self.is_running:
            self.refresh_screen()
            self.game_physic.collide(self.player.position, (10, 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            self.clock.tick(120)

        self.internet_manager.stop()
        pygame.quit()

game = Game()
game.run()