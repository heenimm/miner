import pygame
from config import WINDOW_HEIGHT, WINDOW_WIDTH

pygame.init()
font = pygame.font.SysFont("arial", 24)

flag_img = pygame.image.load("images/flag.png")
mine_img = pygame.image.load("images/bug.png")
smile_img = pygame.image.load("images/smile.png")
dead_img = pygame.image.load("images/cross.png")
win_img = pygame.image.load("images/happy.png")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
