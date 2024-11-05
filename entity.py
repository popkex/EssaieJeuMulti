import pygame

class Entity:
    def __init__(self, game, position=(0, 0), scale=5):
        self.game = game
        self.screen = self.game.screen
        self.position = position
        self.scale = scale


    def draw(self, position):
        """Dessine le joueur"""
        if position:
            self.position = position  # met à jour les positions

        self.move()

        self.image = pygame.draw.rect(self.screen.window, (255, 255, 255), (self.position[0], self.position[1], self.scale, self.scale))


    def move(self, position=None):
        """Déplace le joueur sans l'afficher (permettre au server de s'actualiser)"""
        keys = pygame.key.get_pressed()

        if position:
            x, y = position
        else:
            x, y = self.position

        if keys[pygame.K_UP]:
            y += 1
        if keys[pygame.K_DOWN]:
            y -= 1

        self.position = (x, y)