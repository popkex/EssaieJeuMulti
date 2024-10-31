import pygame

class Entity:
    def __init__(self, game, position=(0, 0), scale=50):
        self.game = game
        self.screen = self.game.screen
        self.position = position
        self.scale = scale

    def draw(self):
        self.image = pygame.draw.rect(self.screen.window, (255, 255, 255), (self.position[0], self.position[1], self.scale, self.scale))
