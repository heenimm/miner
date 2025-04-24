import pygame

from config import WINDOW_WIDTH
from end_window import EndWindow
from game_window import Miner
from start_window import StartWindow


def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH + 64))
    pygame.display.set_caption("Сапер")
    start_window = StartWindow()
    end_window = None
    game = Miner()
    running = True
    game_started = False
    while running:
        screen.fill((0, 0, 0))
        if not game_started:
            start_window.draw()
        else:
            if not game.game_over:
                game.draw()
            else:
                end_window = EndWindow(game.win, int(game.end_time - game.start_time), game.score)
                end_window.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started and start_window.check_start(event.pos):
                    game.reset()
                    game_started = True
                elif game.game_over and end_window.check_restart(event.pos):
                    game.reset()
                    game_started = True
                elif game_started:
                    game.handle_click(event.pos, event.button == 3)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
