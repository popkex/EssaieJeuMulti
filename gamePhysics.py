import pygame
from dataclasses import dataclass

@dataclass
class DataBase:
    walls_collide = []  # Sous la forme : [(x, y, w, h)]



class GamePhysic:

    def __init__(self):
        self.data_base = DataBase()

        self.init_walls()

    def init_walls(self):
        self.data_base.walls_collide = [
            (100, 100, 100, 100)  # (x, y, w, h)
        ]

    def collide(self, entity_position, entity_size) -> str:
        """gerer les collision entre 2entités"""
        zone_collide = []  # "left", "right", "top", "bottom"

        for wall_collide in self.data_base.walls_collide:
            # Récuperation des coordonées du mur
            wall_position = wall_collide[0:2]  # Recuperer x, y
            wall_size = wall_collide[2:4]  # recuperer w, h (largeur, hauteur)

            # Calculer le centre en x et y du mur
            center_wall_x = wall_position[0] + (wall_size[0] / 2)
            center_wall_y = wall_position[1] + (wall_size[1] / 2)

            # Calculer le centre en x et y de l'entité
            center_entity_x = entity_position[0] + (entity_size[0] / 2)
            center_entity_y = entity_position[1] + (entity_size[1] / 2)

            if True:  # """""""""""""""""""""""""""""Vérifier la distance entre le mur et l'entité ici"""""""""""""""""""""""""""""
                """quand le mur se trouve est suffisamment proche du joueur"""
                # vérification de si l'entité touche le mur
                if entity_position[0] < wall_position[0]:
                    """quand l'entité se trouve a droite"""
                    distance_center = center_wall_x - center_entity_x

                    if -5 <= distance_center <= 10:
                        zone_collide.append("right")

                if entity_position[0] > wall_collide[0]:
                    """quand l'entité se trouve a gauche"""
                    distance_center = center_entity_x - center_wall_x

                    if -5 <= distance_center <= 10:
                        zone_collide.append("left")

                if entity_position[1] < wall_position[1]:
                    """quand l'entité se trouve en haut"""
                    distance_center = center_wall_y - center_entity_y

                    if -5 <= distance_center <= 10:
                        zone_collide.append("top")

                if entity_position[1] > wall_position[1]:
                    """quand l'entité se trouve en bast"""
                    distance_center = center_wall_y - center_entity_y

                    if -5 <= distance_center <= 10:
                        zone_collide.append("bottom")

            print(zone_collide)
            return zone_collide