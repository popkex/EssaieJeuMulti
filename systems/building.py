import pygame
from dataclasses import dataclass

@dataclass
class Data:
    name: str
    position: list[int, int]
    lvl: int
    size: list[int, int]
    orientation: int  # Compris entre 0 et 3 || 0: nord; 1: est; 2: sud; 3:ouest
    price: int
    img: pygame.image


class Drill():

    def __init__(self, position, lvl=1, orientation=0):
        name = "drill"
        position = position
        lvl = lvl
        size = [100, 100]
        orientation = orientation
        price = 0
        img = pygame.image.load(r"C:\\Users\\cleme\\Downloads\\i.jpg")

        self.data = Data(name, position, lvl, size, orientation, price, img)

        self.ressource = 0


    def extract_resource(self):
        self.ressource += 1
        print(self.ressource)