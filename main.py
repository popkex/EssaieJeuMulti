import pygame
from screen import Screen
from internetManager import InternetManager

pygame.init()

class Game:
    def __init__(self):
        self.screen = Screen()
        self.internet_manager = InternetManager(self.screen)

        self.is_running = True

    def run(self):
        while self.is_running:
            self.screen.window.fill(False)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

        pygame.quit()

game = Game()
game.run()