import pygame
from screen import Screen
from entity import Entity
from internetManager import InternetManager

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen()
        self.player = Entity(self, position=(50, 50), scale=200)
        self.internet_manager = InternetManager(self)

        self.is_running = True

    def run(self):
        while self.is_running:
            self.screen.window.fill(False)
            self.player.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

        self.internet_manager.stop()
        pygame.quit()

game = Game()
game.run()