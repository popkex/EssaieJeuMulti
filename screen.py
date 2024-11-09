import pygame

class Screen:

    def __init__(self):
        self.window = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("test jeu multi")


    def show_text(self, text, font=100):
        path = r'font\Arialic Hollow.ttf' #aucune dispo pour l'instant
        font = pygame.font.SysFont(path, font, True)
        txt_surface = font.render(text, False, (255, 255, 255))

        self.window.blit(txt_surface, (0, 0))


    def draw_players(self, physics_database, players_pos, local_player_pos):
        """Dessine les joueurs"""
        entity_size = (50, 50)

        physics_database.players_collide.clear()

        if players_pos:
            for player_id, position in players_pos:
                # dessine le joueur
                self.draw_rect(color=(255, 255, 255), pos=position, size=entity_size)
                pygame.draw.rect(self.window, (255, 255, 255), (position[0], position[1], entity_size[0], entity_size[1]))

                # ajoute les collisions
                if players_pos != local_player_pos:
                    (x, y), (w, h) = position, entity_size
                    physics_database.players_collide.append((x, y, w, h))

    def draw_walls(self, walls_pos):
        for wall in walls_pos:
            pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(walls_pos[0][0], walls_pos[0][1], walls_pos[0][2], walls_pos[0][3]))

    def draw_line(self, start_line, stop_line, color=(0, 0, 255)):
        pygame.draw.line(self.window, color, start_line, stop_line, width=5)

    def draw_rect(self, color, pos, size):
        pygame.draw.rect(self.window, color, (pos[0], pos[1], size[0], size[1]))

    def draw_txt(self, txt, police=50, position=(0, 0), center=False, color=(255, 255, 255), render=False, can_blit=True):
        path = "Arial"
        font = pygame.font.SysFont(path, police, True)
        txt_surface = font.render(txt, render, color)

        if center:
            position = txt_surface.get_rect(center=(self.screen.get_width()/2, position[1])) # position 1 signifie le y

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
