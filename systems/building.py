import pygame
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Data:
    name: str
    img: pygame.image
    position: Tuple[int, int]
    lvl: int
    size: Tuple[int, int]
    orientation: int  # Compris entre 0 et 3 || 0: nord; 1: est; 2: sud; 3:ouest
    price: int


class Drill():

    def __init__(self, position, lvl=1, orientation=0):
        name = "drill"
        img = pygame.image.load(r"C:\\Users\\cleme\\Downloads\\i.jpg")
        pos = position
        lvl = lvl
        size = img.get_size()
        ori = orientation
        price = 0

        self.data = Data(
            name=name, 
            img=img,
            position=pos,
            lvl=lvl,
            size=size,
            orientation=ori,
            price=price,
        )

        self.ressource = 0


    def extract_resource(self):
        self.ressource += 1
        print(self.ressource)