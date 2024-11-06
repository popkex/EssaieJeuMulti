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

    def collide(self, entity_position, entity_size):
        for wall_collide in self.data_base.walls_collide:
            wall_position = wall_collide[0:2]  # Recuperer x, y
            wall_size = wall_collide[2:4]  # recuperer w, h (largeur, hauteur)
            print(f"{wall_position}, {wall_size}")