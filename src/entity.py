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

    def draw(self, position=None):
        """Dessine le joueur avec la position mise à jour et applique le décalage de la caméra uniquement pour l'affichage"""
        if position:
            self.position = position  # met à jour les positions

        self.move()  # Déplace le joueur (calculs de déplacements sans caméra)

        # Dessine le joueur à sa position finale (applique la caméra seulement pour l'affichage)
        player_rect = pygame.Rect(self.position[0], self.position[1], self.scale, self.scale)
        player_rect_display = self.game.camera.apply(player_rect)  # Applique le décalage de la caméra uniquement pour l'affichage
        pygame.draw.rect(self.screen.window, (255, 255, 255), player_rect_display)  # Affichage

    def move(self, position=None):
        if position:
            print(position)
        """Déplace le joueur sans appliquer la caméra (calculs de déplacement réels)"""
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

        # Détection des collisions avec les murs (sans décalage caméra)
        zone_collide = self.game.game_physic.collide(self.position, (self.scale, self.scale))
        first_corify_pos = self.rectify_position((x, y), zone_collide)

        zone_collide = self.game.game_physic.collide(first_corify_pos, (self.scale, self.scale), is_building=True)
        second_corify_pos = self.rectify_position(first_corify_pos, zone_collide)

        # Mise à jour de la position du joueur
        self.position = second_corify_pos