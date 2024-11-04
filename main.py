import pygame
from screen import Screen
from entity import Entity
from internetManager import InternetManager

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Entity(self, position=(300, 300), scale=15)
        self.internet_manager = InternetManager()

        self.is_running = True

    def refresh_screen(self):
        """redessine tout l'écran"""
        self.screen.window.fill(False)

        player_pos, other_players_pos = self.internet_manager.get_players_position()
        self.player.draw(player_pos)
        self.player.move()
        self.screen.draw_players(other_players_pos)

        pygame.display.flip()

    def run(self):
        """La bouche de jeu"""
        self.internet_manager.start(self)

        while self.is_running:
            self.refresh_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

        self.internet_manager.stop()
        pygame.quit()

game = Game()
game.run()