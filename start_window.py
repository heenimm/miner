import pygame
from config import WINDOW_WIDTH
from resources import screen, font


class StartWindow:
    def __init__(self):
        self.start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_WIDTH // 2 - 15, 200, 60)

    def draw(self):
        screen.fill((0, 0, 0))
        title_text = font.render("Игра Сапер", True, (255, 255, 255))
        start_text = font.render("Старт", True, (255, 255, 255))
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_WIDTH // 2 - 100))
        pygame.draw.rect(screen, (111, 111, 111), self.start_button)
        screen.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, WINDOW_WIDTH // 2))

    def check_start(self, pos):
        if self.start_button.collidepoint(pos):
            return True
        return False
