import pygame

class Entity:
    def __init__(self, game, position=(0, 0), scale=5):
        self.game = game
        self.screen = self.game.screen
        self.position = position
        self.scale = scale

        self.velocity = 0.5
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity_y = 10
        self.max_velocity_x = 5
        self.default_move_force_x = 10
        self.default_move_force_y = 100
        self.move_force_x = self.default_move_force_x
        self.move_force_y = self.default_move_force_y

        self.tuch_ground = False
        self.player_as_jump = False


    def draw(self, position):
        """Dessine le joueur"""
        if position:
            self.position = position  # met à jour les positions

        self.move()

        self.image = pygame.draw.rect(self.screen.window, (255, 255, 255), (self.position[0], self.position[1], self.scale, self.scale))


    def rectify_position(self, new_position, zone_collide):
        """Applique les collisions pour ajuster la position"""
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
        if position:
            x, y = position
        else:
            x, y = self.position

        """Calculer la force de deplacement"""
        if pygame.K_UP in self.game.key_pressed and self.tuch_ground:
            self.velocity_y -= self.move_force_y
            self.player_as_jump = True
        if pygame.K_LEFT in self.game.key_pressed:
            self.velocity_x -= self.move_force_x
        if pygame.K_RIGHT in self.game.key_pressed:
            self.velocity_x += self.move_force_x
        if not (pygame.K_RIGHT in self.game.key_pressed) and not (pygame.K_LEFT in self.game.key_pressed):
            self.velocity_x = 0

        """Vérifier et corriger si ca velocity si le joueur va trop vite"""
        if not self.player_as_jump and not self.tuch_ground:
            if self.velocity_y >= self.max_velocity_y:
                self.velocity_y = self.max_velocity_y
            elif self.velocity_y <= -self.max_velocity_y:
                self.velocity_y = -self.max_velocity_y

        if self.velocity_x >= self.max_velocity_x:
            self.velocity_x = self.max_velocity_x
        elif self.velocity_x <= -self.max_velocity_x:
            self.velocity_x = -self.max_velocity_x
        else:
            self.velocity_x = 0

        """Appliquer la gravité"""
        self.velocity_x, self.velocity_y = self.game.game_physic.gravity((self.velocity_x, self.velocity_y))

        """Applique la force de deplacement"""
        x += self.velocity_x
        y += self.velocity_y

        # Reset la force quand le joueur touche le sol
        if self.tuch_ground:
            self.velocity_y = 0

        """Applique les collisions"""
        detect_is_ground = []

        # detection des collisions avec les murs
        zone_collide = self.game.game_physic.collide((x, y), (self.scale, self.scale))
        first_corify_pos = self.rectify_position((x, y), zone_collide)
        detect_is_ground.append(True if "bottom" in zone_collide else False)

        # detecte la collisions avec les joueurs
        # zone_collide = self.game.game_physic.collide(entity_position=first_corify_pos, entity_size=(self.scale, self.scale), is_player=True)
        # second_corify_pos = self.rectify_position(first_corify_pos, zone_collide)

        # si le joueur touche le sol dire qu'il le touche
        if True in detect_is_ground:
            self.tuch_ground = True
            self.player_as_jump = False
        else:
            self.tuch_ground = False

        # Mise à jour de la position finale
        self.position = first_corify_pos
