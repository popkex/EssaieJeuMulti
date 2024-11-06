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


    def draw_players(self, players_pos):
        """Dessine les joueurs"""
        if players_pos:
            for player_id, position in players_pos:
                pygame.draw.rect(self.window, (255, 255, 255), (position[0], position[1], 50, 50))

    def draw_walls(self, walls_pos):
        for wall in walls_pos:
            pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(walls_pos[0][0], walls_pos[0][1], walls_pos[0][2], walls_pos[0][3]))