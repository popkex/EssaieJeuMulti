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