import pygame
import sys
from game_window import Miner
from resources import screen

clock = pygame.time.Clock()
game = Miner()

def main():
    while True:
        screen.fill((0, 0, 0))
        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                game.handle_click(event.pos, right_click=event.button == 3)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
