import pygame

class Entity:
    def __init__(self, game, position=(0, 0), scale=5):
        self.game = game
        self.screen = self.game.screen
        self.position = position
        self.scale = scale

        self.velocity = 1


    def draw(self, position):
        """Dessine le joueur"""
        if position:
            self.position = position  # met à jour les positions

        self.move()

        self.image = pygame.draw.rect(self.screen.window, (255, 255, 255), (self.position[0], self.position[1], self.scale, self.scale))


    def rectify_position(self, new_position, zone_collide):
        # Applique les collisions pour ajuster la position
        x, y = new_position

        if "left" in zone_collide and x < self.position[0]:
            x = self.position[0]  # Bloque le déplacement vers la gauche
        if "right" in zone_collide and x > self.position[0]:
            x = self.position[0]  # Bloque le déplacement vers la droite
        if "top" in zone_collide and y < self.position[1]:
            y = self.position[1]  # Bloque le déplacement vers le haut
        if "bottom" in zone_collide and y > self.position[1]:
            y = self.position[1]  # Bloque le déplacement vers le bas

        return (x, y)

    def move(self, position=None):
        """Déplace le joueur sans l'afficher (permettre au server de s'actualiser)"""
        keys = pygame.key.get_pressed()

        if position:
            x, y = position
        else:
            x, y = self.position

        if keys[pygame.K_UP]:
            y -= self.velocity
        if keys[pygame.K_DOWN]:
            y += self.velocity
        if keys[pygame.K_LEFT]:
            x -= self.velocity
        if keys[pygame.K_RIGHT]:
            x += self.velocity

        # detection des collisions avec les murs
        zone_collide = self.game.game_physic.collide(self.position, (self.scale, self.scale))
        first_corify_pos = self.rectify_position((x, y), zone_collide)
        # detecte la collisions avec les joueurs
        zone_collide = self.game.game_physic.collide(entity_position=first_corify_pos, entity_size=(self.scale, self.scale), is_player=True)
        second_corify_pos = self.rectify_position(first_corify_pos, zone_collide)

        # Mise à jour de la position finale
        self.position = second_corify_pos
