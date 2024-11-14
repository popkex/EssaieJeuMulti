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
        self.max_velocity_x = 5
        self.max_velocity_y = 5
        self.move_force_x = self.max_velocity_x
        self.move_force_y = self.max_velocity_y
        self.jump_time = 0

        self.tuch_ground = False
        self.player_as_jump = False


    def draw(self, position):
        """Dessine le joueur"""
        if position:
            self.position = position  # met à jour les positions

        self.move()

        self.image = pygame.draw.rect(self.screen.window, (255, 255, 255), (self.position[0], self.position[1], self.scale, self.scale))

    def rectify_position(self, new_position, zone_collide, wall):
        """Corrige la position du joueur en tenant compte des collisions, en priorisant un seul axe."""
        wx, wy, ww, wh, _ = wall  # Coordonnées du mur
        x, y = new_position

        # Calculer la profondeur d'intersection sur chaque axe
        intersection_x = min(abs(x - (wx + ww)), abs(x + self.scale - wx))
        intersection_y = min(abs(y - (wy + wh)), abs(y + self.scale - wy))

        # Prioriser l'axe avec la plus grande intersection
        if intersection_x < intersection_y:
            # Corriger d'abord l'axe X
            if "left" in zone_collide:
                x = wx + ww  # Place le joueur juste à droite du mur
            elif "right" in zone_collide:
                x = wx - self.scale  # Place le joueur juste à gauche du mur
        else:
            # Corriger d'abord l'axe Y
            if "top" in zone_collide:
                y = wy + wh  # Place le joueur juste en dessous du mur
            elif "bottom" in zone_collide:
                y = wy - self.scale  # Place le joueur juste au-dessus du mur

        return (x, y)




        return (x, y)

    def move(self, position=None):
        """Déplace le joueur sans l'afficher (permettre au serveur de s'actualiser)"""
        if position:
            x, y = position
        else:
            x, y = self.position

        # Calculer la force de déplacement
        if pygame.K_UP in self.game.key_pressed and self.tuch_ground:
            if not self.player_as_jump:
                self.velocity_y -= self.move_force_y
                self.jump_time = 0
                self.player_as_jump = True

        if pygame.K_UP in self.game.key_pressed and self.player_as_jump and self.jump_time < 10:
            self.velocity_y -= 1
            self.jump_time += 1

        if pygame.K_LEFT in self.game.key_pressed:
            self.velocity_x -= self.move_force_x
        if pygame.K_RIGHT in self.game.key_pressed:
            self.velocity_x += self.move_force_x
        if not (pygame.K_RIGHT in self.game.key_pressed) and not (pygame.K_LEFT in self.game.key_pressed):
            self.velocity_x = 0

        if self.velocity_x >= self.max_velocity_x:
            self.velocity_x = self.max_velocity_x
        elif self.velocity_x <= -self.max_velocity_x:
            self.velocity_x = -self.max_velocity_x

        # Appliquer la gravité
        if self.tuch_ground:
            self.velocity_x, self.velocity_y = self.game.game_physic.gravity((self.velocity_x, self.velocity_y), reset_force=True)
        else:
            self.velocity_x, self.velocity_y = self.game.game_physic.gravity((self.velocity_x, self.velocity_y))

        # Appliquer la force de déplacement
        x += self.velocity_x
        y += self.velocity_y

        # Applique les collisions
        zone_collide, wall = self.game.game_physic.collide((x, y), (self.scale, self.scale))

        # Vérifier si un mur a été trouvé avant de corriger la position
        if wall is not None:
            first_corrected_pos = self.rectify_position((x, y), zone_collide, wall)
        else:
            first_corrected_pos = (x, y)

        # Mise à jour de la position finale
        self.position = first_corrected_pos

        # Détection du sol
        # si le joueur touche le sol dire qu'il le touche
        if "bottom" in zone_collide:
            self.tuch_ground = True
            self.player_as_jump = False
        else:
            self.tuch_ground = False


        if "top" in zone_collide:
            self.velocity_y = 0
