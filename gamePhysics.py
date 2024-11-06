import pygame
from dataclasses import dataclass

@dataclass
class DataBase:
    walls_collide = []  # Sous la forme : [(x, y, w, h)]



class GamePhysic:

    def __init__(self, screen):
        self.debug_mode = False
        self.data_base = DataBase()
        self.screen = screen
        
        self.secure_dist_collide = 2

        self.init_walls()

    def init_walls(self):
        self.data_base.walls_collide = [
            (100, 100, 100, 100)  # (x, y, w, h)
        ]

    def collide(self, entity_position, entity_size) -> str:
        """gerer les collision entre 2entités"""
        zone_collide = []  # "left", "right", "top", "bottom"

        for wall_collide in self.data_base.walls_collide:
            """summary
                point a = top_left of the wall
                point b = top_right of the wall
                point c = bottom_right of the wall
                point d = bottom_left of the wall

                aex, aey, bex, bey, cex, cey, dex, dey => position du coin (a, b, c, d) suivie de e (entity) suivie de x ou y  
                awx, awy, bwx, bwy, cwx, cwy, dwx, dwy => position du coin (a, b, c, d) suivie de w (wall) suivie de x ou y  
            """

            # Récuperation des coordonées du mur
            wall_position = wall_collide[0:2]  # Recuperer x, y
            wall_size = wall_collide[2:4]  # recuperer w, h (largeur, hauteur)

            # Récupérer les coins de l'entité
            aex, aey = entity_position
            bex, bey = entity_position[0] + entity_size[0], entity_position[1]
            cex, cey = entity_position[0] + entity_size[0], entity_position[1] + entity_size[1]
            dex, dey = entity_position[0], entity_position[1] + entity_size[1]

            # Recupérer les coins du mur
            awx, awy = wall_position
            bwx, bwy = wall_position[0] + wall_size[0], wall_position[1]
            cwx, cwy = wall_position[0] + wall_size[0], wall_position[1] + wall_size[1]
            dwx, dwy = wall_position[0], wall_position[1] + wall_size[1]

            #region Debug
            if self.debug_mode:
                # print(f"a: {aex, aey}, b: {bex, bey}, c: {cex, cey}, d: {dex, dey}")
                self.screen.draw_line((aex, aey), (bex, bey))
                self.screen.draw_line((cex, cey), (dex, dey))
                self.screen.draw_line((aex, aey), (dex, dey))
                self.screen.draw_line((bex, bey), (cex, cey))

                self.screen.draw_line((awx, awy), (bwx, bwy))
                self.screen.draw_line((cwx, cwy), (dwx, dwy))
                self.screen.draw_line((awx, awy), (dwx, dwy))
                self.screen.draw_line((bwx, bwy), (cwx, cwy))

                pygame.display.flip()
            #endregion

            # Check les collisions
            ## collision bas entité (haut mur)
            if (awx - self.secure_dist_collide < dex < bwx + self.secure_dist_collide and awy - self.secure_dist_collide < dey < bwy + self.secure_dist_collide) or (awx - self.secure_dist_collide < cex < bwx + self.secure_dist_collide and awy - self.secure_dist_collide < cey < bwy + self.secure_dist_collide):
                zone_collide.append("bottom")
            ## collision haut entité (bas mur)
            if (dwx - self.secure_dist_collide < aex < cwx + self.secure_dist_collide and dwy - self.secure_dist_collide < aey < cwy + self.secure_dist_collide) or (dwx - self.secure_dist_collide < bex < cwx + self.secure_dist_collide and dwy - self.secure_dist_collide < bey < cwy + self.secure_dist_collide):
                zone_collide.append("top")
            ## collision droit entité (gauche mur)
            if (awx - self.secure_dist_collide < bex < dwx + self.secure_dist_collide and awy - self.secure_dist_collide < bey < dwy + self.secure_dist_collide) or (awx - self.secure_dist_collide < cex < dwx + self.secure_dist_collide and awy - self.secure_dist_collide < cey < dwy + self.secure_dist_collide):
                zone_collide.append("right")
            ## collision gauche entité (droite mur)
            if (bwx - self.secure_dist_collide < aex < cwx + self.secure_dist_collide and bwy - self.secure_dist_collide < aey < cwy + self.secure_dist_collide) or (bwx - self.secure_dist_collide < dex < cwx + self.secure_dist_collide and bwy - self.secure_dist_collide < dey < cwy + self.secure_dist_collide):
                zone_collide.append("left")

        return zone_collide