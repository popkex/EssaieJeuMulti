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