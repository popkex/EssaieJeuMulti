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
        for wall_collide in self.data_base.walls_collide:
            # Récuperation des coordonées du mur
            wall_position = wall_collide[0:2]  # Recuperer x, y
            wall_size = wall_collide[2:4]  # recuperer w, h (largeur, hauteur)

            if True:  # Vérifier la distance entre le mur et l'entité ici
                # vérification de si l'entité touche le mur
                ## si les 2 position x sont diff
                if entity_position[0] != wall_position[0]:
                    # Calculer l'espacement x entre les 2 positions
                    if entity_position[0] > wall_position[0]:
                        """regarde si la position du joueur est plus grande, donc se trouve a droite 
                            faire le calcule adequate pour cela (x_spacing = entity_position[0] - wall_position[0] ou inverser les 2)
                        """
                else:
                    """renvoyer, touche le mur a droite"""

                ## si les 2 position y sont diff
                if entity_position[1] != wall_position[1]:
                    pass