import pygame
import random
import time
from tile import Tile
from config import GRID_SIZE, NUM_MINES, TILE_SIZE, WINDOW_WIDTH
from resources import smile_img, dead_img, win_img, font, screen

class Miner:
    def __init__(self):
        self.grid = [[Tile(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        self.mines = set()
        self.started = False
        self.game_over = False
        self.win = False
        self.start_time = None
        self.end_time = None
        self.reset_button = pygame.Rect(WINDOW_WIDTH // 2 - 16, 5, 32, 32)
        self.score = 0
        self.reset()

    def reset(self):
        self.started = False
        self.game_over = False
        self.win = False
        self.start_time = None
        self.end_time = None
        self.score = 0
        self.mines.clear()
        for row in self.grid:
            for tile in row:
                tile.__init__(tile.x, tile.y)
        self.place_mines()

    def place_mines(self):
        while len(self.mines) < NUM_MINES:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if not self.grid[x][y].is_mine:
                self.grid[x][y].is_mine = True
                self.mines.add((x, y))
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if not self.grid[x][y].is_mine:
                    self.grid[x][y].adjacent = sum(
                        self.grid[nx][ny].is_mine
                        for nx in range(max(0, x - 1), min(GRID_SIZE, x + 2))
                        for ny in range(max(0, y - 1), min(GRID_SIZE, y + 2))
                        if (nx, ny) != (x, y)
                    )

    def reveal(self, x, y):
        tile = self.grid[x][y]
        if tile.revealed or tile.flagged:
            return
        tile.revealed = True
        if tile.is_mine:
            self.win = False
            self.game_over = True
            self.end_time = time.time()
            self.reveal_all()
            return
        self.score += 1
        if tile.adjacent == 0:
            for nx in range(max(0, x - 1), min(GRID_SIZE, x + 2)):
                for ny in range(max(0, y - 1), min(GRID_SIZE, y + 2)):
                    if not self.grid[nx][ny].revealed:
                        self.reveal(nx, ny)

    def check_win(self):
        for row in self.grid:
            for tile in row:
                if not tile.is_mine and not tile.revealed:
                    return
        self.win = True
        self.game_over = True
        self.end_time = time.time()
        self.reveal_all()

    def reveal_all(self):
        for row in self.grid:
            for tile in row:
                tile.revealed = True

    def handle_click(self, pos, right_click):
        if self.reset_button.collidepoint(pos):
            self.reset()
            return
        if self.game_over:
            return

        x = pos[0] // TILE_SIZE
        y = (pos[1] - 64) // TILE_SIZE
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return

        tile = self.grid[x][y]
        if right_click:
            if not tile.revealed:
                tile.flagged = not tile.flagged
        else:
            if not self.started:
                self.started = True
                self.start_time = time.time()
            self.reveal(x, y)

        if not self.game_over:
            self.check_win()

    def draw(self):
        pygame.draw.rect(screen, (34, 45, 34), (0, 0, WINDOW_WIDTH, 80))
        face = win_img if self.game_over and self.win else dead_img if self.game_over else smile_img
        screen.blit(face, self.reset_button.topleft)
        flags = sum(tile.flagged for row in self.grid for tile in row)
        bomb_text = font.render(f"Мины: {NUM_MINES - flags}", True, (255, 255, 255))
        screen.blit(bomb_text, (10, 20))
        elapsed = int(time.time() - self.start_time) if self.started and not self.end_time else int(self.end_time - self.start_time) if self.end_time else 0
        time_text = font.render(f"Время: {elapsed}", True, (255, 255, 255))
        screen.blit(time_text, (WINDOW_WIDTH - 120, 20))
        score_text = pygame.font.SysFont("arial", 18).render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (WINDOW_WIDTH // 2 - 30, 40))

        for row in self.grid:
            for tile in row:
                tile.draw()
