import pygame
from typing import Tuple

class Screen:

    def __init__(self, game):
        self.game = game

        self.case = {}

        world_width, world_height = 5000, 9000

        self.camera = Camera(1080, 720, world_width, world_height)  # Assurez-vous que world_width et world_height sont appropriés

        self.window = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("test jeu multi")


    def add_building(self, building_class, id, case):
        self.case[id] = (case, building_class) 

    def get_index_case_with_name(self, building_id):
        for i, build in enumerate(self.case):
            build_id = build.data.id

            if building_id == build_id:
                return i

    def convert_case_to_rect(self, case):
        """une case fait du 8par8"""
        result = None

        if len(case) == 2:
            result = case[0] * 16, case[1] * 16
        elif len(case) == 4:
            result = case[0] * 16, case[1] * 16, case[2] * 16, case[3] * 16
        else:
            print("\033[31m" + f"il y a {len(case)} élements fournis dans {case}, cette longueur devrait etre de 2 ou 4" + "\033[0m")

        return result

    def convert_rect_to_case(self, rect):
        """une case fait du 16 par 16"""
        result = None

        if len(rect) == 2:
            result = int(rect[0] / 16), int(rect[1] / 16)
        elif len(rect) == 4:
            result = int(rect[0] / 16), int(rect[1] / 16), int(rect[2] / 16), int(rect[3] / 16)
        else:
            print("\033[31m" + f"screen.convert_rect_to_case(): il y a {len(rect)} élements fournis dans {rect}, cette longueur devrait etre de 2 ou 4" + "\033[0m")

        return result


    def refresh_screen(self, player_pos=Tuple, all_players_pos=[], is_online=True):
        """Redessine l'écran avec la caméra qui suit le joueur."""
        self.window.fill(False)

        # Crée un rectangle pour le joueur local
        if player_pos:
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

            # Mettez à jour la caméra avec la position du joueur local
            self.camera.update(player_rect)

        # Dessinez les murs
        self.draw_walls()

        # Dessinez les batiments
        self.draw_building()

        if is_online:
            # Dessinez les joueurs (tous les joueurs, y compris le local)
            self.draw_players(players_pos=all_players_pos)
        else:
            self.draw_players(player_pos=self.game.player.position)  # mettre la pos du joueur

        if self.game.game_physic.debug_mode: 
            self.debug_mode()


    def show_text(self, text, font=100):
        path = r'font\Arialic Hollow.ttf' #aucune dispo pour l'instant
        font = pygame.font.SysFont(path, font, True)
        txt_surface = font.render(text, False, (255, 255, 255))

        self.window.blit(txt_surface, (0, 0))


    def draw_players(self, players_pos=None, player_pos=None):
        entity_size = (50, 50)  # Dimensions de chaque joueur

        physics_database = self.game.game_physic.data_base
        physics_database.players_collide.clear()

        if not players_pos and player_pos:
            """si on est en solo"""
            self.apply_player(position=player_pos, entity_size=entity_size)
        elif players_pos and not player_pos:
            """si on est en multi"""
            for player_id, position in players_pos:
                self.apply_player(position, entity_size)
        else:
            print("Merci de donner une position d'un ou plusieurs joueurs dans le draw_player (screen.py)")
            pass

    def apply_player(self, position: Tuple[int, int], entity_size):
        """Permet de modifier la position des entitées en fonction du positionnement de la cam"""
        physics_database = self.game.game_physic.data_base

        # Déplace les entités en fonction de la caméra
        player_rect = pygame.Rect(position[0], position[1], entity_size[0], entity_size[1])
        player_rect = self.camera.apply(player_rect)  # Applique la transformation de la caméra à la position du joueur

        self.draw_rect(color=(255, 255, 255), pos=player_rect.topleft, size=entity_size)

        # Ajoute les collisions
        (x, y), (w, h) = player_rect.topleft, entity_size
        physics_database.players_collide.append((x, y, w, h))


    def draw_walls(self):
        walls_data = self.game.game_physic.data_base.walls_collide

        for wall in walls_data:
            # Recuperer les coordonées reels du mur
            x, y, w, h = self.convert_case_to_rect(wall[0:4])

            # Applique la transformation de la caméra aux murs
            wall_rect = pygame.Rect(x, y, w, h)
            wall_rect = self.camera.apply_rect(wall_rect)  # Applique le décalage de la caméra
            pygame.draw.rect(self.window, wall[4], wall_rect)

    def draw_building(self):
        """Afficher tout les buildings"""
        for building in self.game.building.data.all_building:
            building_data = building.data

            img = building_data.img
            size = building_data.size
            position = building_data.position

            x, y = position
            h, w = size

            # Recuperer les coordonées reels du building
            x, y, h, w = self.convert_case_to_rect((x, y, h, w))

            building_rect = pygame.Rect(x, y, h, w)

            position = self.camera.apply_rect(building_rect)  # Applique le décalage de la caméra

            img = pygame.transform.scale(img, (h, w))

            self.window.blit(img, position)

        """Afficher le buildings en cours de positionnement"""
        img = self.game.building.data.previous_building

        if img:
            img, rect = img

            self.window.blit(img, rect)


    def draw_line(self, start_line, stop_line, color=(0, 0, 255)):
        pygame.draw.line(self.window, color, start_line, stop_line, width=5)

    def draw_rect(self, color, pos, size):
        pygame.draw.rect(self.window, color, (pos[0], pos[1], size[0], size[1]))

    def draw_txt(self, txt, police=50, position=(0, 0), center=False, color=(255, 255, 255), render=False, can_blit=True):
        path = "Arial"
        font = pygame.font.SysFont(path, police, True)
        txt_surface = font.render(txt, render, color)

        if center:
            position = txt_surface.get_rect(center=(self.get_width()/2, position[1])) # position 1 signifie le y

        if can_blit:
            self.window.blit(txt_surface, position)
        return txt_surface, position


    def debug_mode(self):
        """
        /!\ ceci est une partie du mode debug, une partie se trouve dans le gamePhysic.py et affiche les collisions /!\ 
        affiche les informations du debug mode (comme les fps)
        """
        text = f'{int(self.game.clock.get_fps())}fps'
        txt_surface = self.draw_txt(text, police=10)
        txt_surface = (txt_surface[0].get_rect())
        pygame.display.update(txt_surface)



class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.world_size = pygame.Rect(0, 0, world_width, world_height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Déplace les entités en appliquant la position de la caméra."""
        return entity.move(self.camera.topleft)

    def apply_rect(self, rect):
        """Applique le déplacement de la caméra à un rectangle donné."""
        return rect.move(self.camera.topleft)

    def update(self, target):
        """Met à jour la position de la caméra pour suivre le joueur."""
        # La caméra doit être centrée sur le joueur (target).
        x = -target.centerx + self.width // 2
        y = -target.centery + self.height // 2

        # Limites de la caméra : empêcher qu'elle dépasse les bords du monde
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_size.width - self.width), x)
        y = max(-(self.world_size.height - self.height), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)