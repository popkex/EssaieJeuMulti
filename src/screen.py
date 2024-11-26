import pygame

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
        """une case fait du 16par16"""
        x, y = case[0] * 16, case[1] * 16

        return (x, y)

    def convert_rect_to_case(self, rect):
        """une case fait du 16 par 16"""
        x, y = int(rect[0] / 16), int(rect[1] / 16)

        return (x, y)


    def refresh_screen(self, player_pos, all_players_pos, d):
        """Redessine l'écran avec la caméra qui suit le joueur."""
        self.window.fill(False)

        # Crée un rectangle pour le joueur local
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)

        # Mettez à jour la caméra avec la position du joueur local
        self.camera.update(player_rect)

        # Dessinez les murs
        self.draw_walls(self.game.game_physic.data_base.walls_collide)

        # Dessinez les batiments
        self.draw_building()


        # Dessinez les joueurs (tous les joueurs, y compris le local)
        self.draw_players(self.game.game_physic.data_base, all_players_pos)

        # Déplace le joueur local
        self.game.player.move()

        if not self.game.game_physic.debug_mode: 
            pygame.display.flip()
        else:
            self.debug_mode(self.game.clock)


    def show_text(self, text, font=100):
        path = r'font\Arialic Hollow.ttf' #aucune dispo pour l'instant
        font = pygame.font.SysFont(path, font, True)
        txt_surface = font.render(text, False, (255, 255, 255))

        self.window.blit(txt_surface, (0, 0))

    def draw_players(self, physics_database, players_pos):
        """Dessine les joueurs en tenant compte du décalage de la caméra."""
        entity_size = (50, 50)  # Dimensions de chaque joueur

        physics_database.players_collide.clear()

        for player_id, position in players_pos:
            # Déplace les entités en fonction de la caméra
            player_rect = pygame.Rect(position[0], position[1], entity_size[0], entity_size[1])
            player_rect = self.camera.apply(player_rect)  # Applique la transformation de la caméra à la position du joueur

            self.draw_rect(color=(255, 255, 255), pos=player_rect.topleft, size=entity_size)

            # Ajoute les collisions
            (x, y), (w, h) = player_rect.topleft, entity_size
            physics_database.players_collide.append((x, y, w, h))

    def draw_walls(self, walls_data):
        for wall in walls_data:
            # Recuperer les coordonées reels du mur
            wall_rect = self.convert_case_to_rect(wall[0:3]
)
            # Applique la transformation de la caméra aux murs
            wall_rect = pygame.Rect(wall[0], wall[1], wall[2], wall[3])
            wall_rect = self.camera.apply_rect(wall_rect)  # Applique le décalage de la caméra
            pygame.draw.rect(self.window, wall[4], wall_rect)


    def draw_building(self):
        for building in self.game.building.data.all_building:
            building_data = building.data

            # Recuperer les coordonées reels du building
            position = self.convert_case_to_rect(building_data.position)

            img = building_data.img
            size = building_data.size
            position = building_data.position

            building_rect = pygame.Rect(position[0], position[1], size[0], size[1])

            position = self.camera.apply_rect(building_rect)  # Applique le décalage de la caméra

            self.window.blit(img, position)


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


    def debug_mode(self, clock):
        """
        /!\ ceci est une partie du mode debug, une partie se trouve dans le gamePhysic.py et affiche les collisions /!\ 
        affiche les informations du debug mode (comme les fps)
        """
        text = f'{int(clock.get_fps())}fps'
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