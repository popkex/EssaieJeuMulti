import pygame
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class BuildingData:
    all_building: list = field(default_factory=list)
    all_drill: list = field(default_factory=list)


@dataclass
class DrillsData:
    name: str
    type: str
    img: pygame.image
    position: Tuple[int, int]
    lvl: int
    size: Tuple[int, int]
    orientation: int  # Compris entre 0 et 3 || 0: nord; 1: est; 2: sud; 3:ouest
    price: int
    max_ressource_stock = int


class Building:
    def __init__(self, game):
        self.game = game

        self.data = BuildingData()

    def add_building(self, building):
        type = building.data.type

        if type == "drill":
            input(building)
            self.data.all_drill.append(building)

        self.data.all_building.append(building)


class Drill(Building):

    def __init__(self, position, lvl=1, orientation=0):
        name = "the drill bg"
        type = "drill"
        img = pygame.image.load(r"C:\\Users\\cleme\\Downloads\\i.jpg")
        pos = position
        lvl = lvl
        size = img.get_size()
        ori = orientation
        price = 0
        max_ressource_stock = 100

        self.data = DrillsData(
            name=name, 
            type=type,
            img=img,
            position=pos,
            lvl=lvl,
            size=size,
            orientation=ori,
            price=price,
        )

        self.init()

    def init(self):
        if buildings:
            buildings.add_building(self)  # enregistre la foreuse
            buildings.game.game_physic.add_building_collide(self.data)  # ajoute les collisions de la foreuse
        else:
            print("\033[38;5;196m" + "Une erreur est survenue, impossible d'initier la forreuse car buildings n'a pas été initier" + "\033[0m")


    def extract_resource(self):
        self.ressource += 1
        print(self.ressource)


#--------------------------------------------------------------------------------------------------
buildings = None