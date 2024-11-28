import pygame
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class BuildingData:
    all_building: list = field(default_factory=list)
    all_drill: list = field(default_factory=list)


@dataclass
class DrillsData:
    id: int
    name: str
    type: str
    img: pygame.image
    position: Tuple[int, int]
    lvl: int
    size: Tuple[int, int]
    orientation: int  # Compris entre 0 et 3 || 0: sud; 1: ouest; 2: nord; 3: est
    price: int
    ressource: int
    max_ressource_stock: int
    ressource_exit: Tuple[int, int]


class Building:
    def __init__(self, game):
        self.game = game

        self.data = BuildingData()

        self.current_id = 0

    def add_building(self, building):
        type = building.data.type

        if type == "drill":
            self.data.all_drill.append(building)

        self.data.all_building.append(building)


    def update_all_building(self):
        for build in self.data.all_building:
            build.update()


    def get_id(self):
        self.current_id += 1
        return self.current_id


class Drill(Building):

    def __init__(self, position, lvl=1, orientation=0):
        id = None
        name = "the drill bg"
        type = "drill"
        img = pygame.image.load(r"Assets\i.png")
        pos = position
        lvl = lvl
        size = img.get_size()
        ori = orientation
        price = 0
        ressource = 0
        max_ressource_stock = 100
        ressource_exit = None

        # Convertir la taille de l'img (qui est en px) en case
        size = size[0] / 16, size[1] / 16

        self.data = DrillsData(
            id=id,
            name=name, 
            type=type,
            img=img,
            position=pos,
            lvl=lvl,
            size=size,
            orientation=ori,
            price=price,
            ressource=ressource,
            max_ressource_stock=max_ressource_stock,
            ressource_exit=self.defi_ressource_exit(ori, pos, size)
        )

        self.init()

    def init(self):
        if buildings:
            self.data.id = buildings.get_id()
            buildings.add_building(self)  # enregistre la foreuse
            buildings.game.game_physic.add_building_collide(self.data)  # ajoute les collisions de la foreuse
        else:
            print("\033[38;5;196m" + "Une erreur est survenue, impossible d'initier la forreuse car buildings n'a pas été initier" + "\033[0m")

    def defi_ressource_exit(self, ori, pos, size):
        # si l'orientation est celle par defaut : sortie vers le sud
        if ori == 0:
            x = int(pos[0] + size[0] / 2)
            y = pos[1] + size[1]
        elif ori == 1:
            x = pos[0]
            y = int(pos[1] + size[1] / 2)
        elif ori == 2:
            x = int(pos[0] + size[0] / 2)
            y = pos[1]
        else:
            x = pos[0] + size[0]
            y = int(pos[1] + size[1] / 2)

        # input(f"ori: {ori}, pos: {pos}, size: {size}, xy: {x, y}")
        return (x, y)


    def extract_resource(self):
        self.data.ressource += 1


    def update(self):
        self.extract_resource()


#--------------------------------------------------------------------------------------------------
buildings = None