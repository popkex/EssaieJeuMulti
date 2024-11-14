import pygame
import math
from dataclasses import dataclass




"""
TODO:
    vérifier la distance pour generer ou non les collisions
"""




@dataclass
class DataBase:
    walls_collide = []  # Sous la forme : [(x, y, w, h)]
    players_collide = []  # Sous la forme : [(x, y, w, h)]



class GamePhysic:

    def __init__(self, screen, game):
        self.game=game
        self.debug_mode = True
        self.data_base = DataBase()
        self.screen = screen

        self.secure_dist_wall_collide = 2
        self.secure_dist_player_collide = 10
        self.dist_generate_wall_collide = 75
        self.dist_generate_player_collide = 75

        self.gravity_force = 0.5
        self.gravity_jump_force = 0.01

        self.init_walls()

    def init_walls(self):
        self.data_base.walls_collide = [
            (0, 700, 2000, 100, (0, 255, 0)),  # (x, y, w, h, (color)) /// le sol

            # les murs pour éviter de sortir du niveau
            (0, 600, 350, 50, (175, 175, 175)),
            (0, 550, 250, 50, (175, 255, 0)),
            (0, 500, 200, 50, (0, 255, 0)),
            (300, 450, 75, 50, (0, 255, 0)),
        ]

    #region Collide
    def collide(self, entity_position, entity_size, is_player=False) -> str:
        if is_player:
            return self.entity_collide(entity_position, entity_size)
        else:
            return self.wall_collide(entity_position, entity_size)

    def wall_collide(self, entity_position, entity_size):
        """Gérer les collisions entre une entité et un mur de manière optimisée, avec debug."""
        zone_collide = []
        collided_wall = None

        ex, ey = entity_position
        ew, eh = entity_size

        for wall in self.data_base.walls_collide:
            wx, wy = wall[0:2]
            ww, wh = wall[2:4]

            entity_left = ex
            entity_right = ex + ew
            entity_top = ey
            entity_bottom = ey + eh

            wall_left = wx
            wall_right = wx + ww
            wall_top = wy
            wall_bottom = wy + wh

            if entity_right < wall_left or entity_left > wall_right or entity_bottom < wall_top or entity_top > wall_bottom:
                wall_is_detected = False
            else:
                wall_is_detected = True

            #region Debug
            if self.debug_mode:
                # Dessiner la boîte englobante de l'entité
                self.screen.draw_line((entity_left, entity_top), (entity_right, entity_top), color=(255, 255, 0))
                self.screen.draw_line((entity_right, entity_top), (entity_right, entity_bottom), color=(255, 255, 0))
                self.screen.draw_line((entity_right, entity_bottom), (entity_left, entity_bottom), color=(255, 255, 0))
                self.screen.draw_line((entity_left, entity_bottom), (entity_left, entity_top), color=(255, 255, 0))

                # Dessiner la boîte englobante du mur
                if wall_is_detected:
                    self.screen.draw_line((wall_left, wall_top), (wall_right, wall_top), color=(0, 255, 255))
                    self.screen.draw_line((wall_right, wall_top), (wall_right, wall_bottom), color=(0, 255, 255))
                    self.screen.draw_line((wall_right, wall_bottom), (wall_left, wall_bottom), color=(0, 255, 255))
                    self.screen.draw_line((wall_left, wall_bottom), (wall_left, wall_top), color=(0, 255, 255))

                pygame.display.flip()
            #endregion

            # Déterminer les côtés de collision
            if wall_is_detected:
                if entity_bottom >= wall_top and entity_top < wall_top:
                    zone_collide.append("bottom")
                    collided_wall = wall
                if entity_top <= wall_bottom and entity_bottom > wall_bottom:
                    zone_collide.append("top")
                    collided_wall = wall
                if entity_right >= wall_left and entity_left < wall_left:
                    zone_collide.append("right")
                    collided_wall = wall
                if entity_left <= wall_right and entity_right > wall_right:
                    zone_collide.append("left")
                    collided_wall = wall

        print(f"zoneCollide: {zone_collide}; collided_wall: {collided_wall}")

        return zone_collide, collided_wall

    def entity_collide(self, entity_position, entity_size):
        """gerer les collision entre une entité et un mur"""
        zone_collide = []  # "left", "right", "top", "bottom"

        for player_collide in self.data_base.players_collide:
            """summary
                point a = top_left of the entity or player
                point b = top_right of the entity or player
                point c = bottom_right of the entity or player
                point d = bottom_left of the entity or player

                aex, aey, bex, bey, cex, cey, dex, dey => position du coin (a, b, c, d) suivie de e (entity) suivie de x ou y  
                apx, apy, bpx, bpy, cpx, cpy, dpx, dpy => position du coin (a, b, c, d) suivie de p (player) suivie de x ou y  

                entity est generalement le joueur local et player les joueurs distants
            """

            player_position = player_collide[0:2]
            player_size = player_collide[2:4]

            # Récupérer les coins de l'entité
            aex, aey = entity_position
            bex, bey = entity_position[0] + entity_size[0], entity_position[1]
            cex, cey = entity_position[0] + entity_size[0], entity_position[1] + entity_size[1]
            dex, dey = entity_position[0], entity_position[1] + entity_size[1]

            # Recupérer les coins du mur
            apx, apy = player_position
            bpx, bpy = player_position[0] + player_size[0], player_position[1]
            cpx, cpy = player_position[0] + player_size[0], player_position[1] + player_size[1]
            dpx, dpy = player_position[0], player_position[1] + player_size[1]

            # calcule la distance de calcule pour les collisions avec le joueur
            dist_max = self.dist_generate_player_collide * (max(entity_size[0], entity_size[1]) % 50 + 1)
            if math.sqrt((aex - apx)**2 + (aey - apy)**2) < dist_max:
                #region Debug
                if self.debug_mode:
                    # print(f"a: {aex, aey}, b: {bex, bey}, c: {cex, cey}, d: {dex, dey}")
                    self.screen.draw_line((apx, apy), (bpx, bpy))
                    self.screen.draw_line((cpx, cpy), (dpx, dpy))
                    self.screen.draw_line((apx, apy), (dpx, dpy))
                    self.screen.draw_line((bpx, bpy), (cpx, cpy))

                    pygame.display.flip()
                #endregion

                # Check les collisions
                ## collision bas entité (haut mur)
                if (apx - self.secure_dist_player_collide < dex < bpx + self.secure_dist_player_collide and apy - self.secure_dist_player_collide < dey < bpy + self.secure_dist_player_collide) or (apx - self.secure_dist_player_collide < cex < bpx + self.secure_dist_player_collide and apy - self.secure_dist_player_collide < cey < bpy + self.secure_dist_player_collide):
                    zone_collide.append("bottom")
                ## collision haut entité (bas mur)
                if (dpx - self.secure_dist_player_collide < aex < cpx + self.secure_dist_player_collide and dpy - self.secure_dist_player_collide < aey < cpy + self.secure_dist_player_collide) or (dpx - self.secure_dist_player_collide < bex < cpx + self.secure_dist_player_collide and dpy - self.secure_dist_player_collide < bey < cpy + self.secure_dist_player_collide):
                    zone_collide.append("top")
                ## collision droit entité (gauche mur)
                if (apx - self.secure_dist_player_collide < bex < dpx + self.secure_dist_player_collide and apy - self.secure_dist_player_collide < bey < dpy + self.secure_dist_player_collide) or (apx - self.secure_dist_player_collide < cex < dpx + self.secure_dist_player_collide and apy - self.secure_dist_player_collide < cey < dpy + self.secure_dist_player_collide):
                    zone_collide.append("right")
                ## collision gauche entité (droite mur)
                if (bpx - self.secure_dist_player_collide < aex < cpx + self.secure_dist_player_collide and bpy - self.secure_dist_player_collide < aey < cpy + self.secure_dist_player_collide) or (bpx - self.secure_dist_player_collide < dex < cpx + self.secure_dist_player_collide and bpy - self.secure_dist_player_collide < dey < cpy + self.secure_dist_player_collide):
                    zone_collide.append("left")

        return zone_collide
    #endregion

    #region Gravity
    def gravity(self, velocity_force, reset_force=False):
        x, y = velocity_force

        if reset_force:
            self.gravity_force = 0
        else:
            # Augmenter la force de gravité progressivement
            self.gravity_force = min(self.gravity_force + 0.025, 0.5)  # Limite à 2 pour éviter une chute trop rapide

        y += self.gravity_force

        return (x, y)

    #endregion
