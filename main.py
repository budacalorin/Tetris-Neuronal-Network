import pygame
import DisplayModule as dm
import GameModule as gm


if __name__ == '__main__':
    displayManager = dm.DisplayManager()
    state = gm.State(
        gm.Table([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 9, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 9, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 8, 8, 5, 4, 0, 0, 2, 1, 0],
            [6, 5, 0, 5, 4, 4, 2, 2, 1, 0],
            [6, 7, 7, 1, 4, 3, 2, 2, 1, 10]
        ])
    )
    displayManager.displayState(state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



