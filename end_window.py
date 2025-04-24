import pygame
from config import WINDOW_WIDTH
from resources import screen, font

class EndWindow:
    def __init__(self, win, time, score):
        self.win = win
        self.time = time
        self.score = score
        self.end_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_WIDTH // 2 + 50, 200, 60)

    def draw(self):
        screen.fill((0, 0, 0))
        result_text = "Вы победили!" if self.win else "Конец игры"
        result_surface = font.render(result_text, True, (255, 255, 255))
        time_surface = font.render(f"Время: {self.time} сек", True, (255, 255, 255))
        score_surface = font.render(f"Очки: {self.score}", True, (255, 255, 255))
        screen.blit(result_surface, (WINDOW_WIDTH // 2 - result_surface.get_width() // 2, WINDOW_WIDTH // 2 - 90))
        screen.blit(time_surface, (WINDOW_WIDTH // 2 - time_surface.get_width() // 2, WINDOW_WIDTH // 2 - 40))
        screen.blit(score_surface, (WINDOW_WIDTH // 2 - score_surface.get_width() // 2, WINDOW_WIDTH // 2))
        pygame.draw.rect(screen, (111, 111, 111), self.end_button)
        restart_surface = font.render("Перезапуск", True, (255, 255, 255))
        screen.blit(restart_surface, (WINDOW_WIDTH // 2 - restart_surface.get_width() // 2, WINDOW_WIDTH // 2 + 60))

    def check_restart(self, pos):
        return self.end_button.collidepoint(pos)
