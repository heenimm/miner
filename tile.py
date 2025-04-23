import pygame
from config import TILE_SIZE
from resources import flag_img, mine_img, font, screen


class Tile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + 64, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y
        self.is_mine = False
        self.adjacent = 0
        self.revealed = False
        self.flagged = False

    def draw(self):
        color = (200, 200, 200) if self.revealed else (100, 100, 100)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (34, 45, 34), self.rect, 1)

        if self.revealed:
            if self.is_mine:
                screen.blit(mine_img, self.rect.topleft)
            elif self.adjacent > 0:
                text = font.render(str(self.adjacent), True, (0, 0, 255))
                screen.blit(text, (self.rect.x + 10, self.rect.y + 5))
        elif self.flagged:
            screen.blit(flag_img, self.rect.topleft)
