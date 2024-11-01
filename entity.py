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

        self.image = pygame.draw.rect(self.screen.window, (255, 255, 255), (self.position[0], self.position[1], self.scale, self.scale))

        self.game.internet_manager.force_send_player_position(self.position)  # force l'actualisation de la position du joueur


    def move(self, position):
        """Déplace le joueur"""
        keys = pygame.key.get_pressed()

        if position:
            x, y = position
        else:
            x, y = self.position

        if keys[pygame.K_UP]:
            y += 5
        if keys[pygame.K_DOWN]:
            y -= 5

        self.draw((x, y))