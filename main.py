import DisplayModule as dm
import GameModule as gm
import time


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

    tetris = gm.TetrisHelper([
        # I
        gm.TetrisPiece([
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)]
        ]),
        # L
        gm.TetrisPiece([
            [(0, 0), (1, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(0, 0), (0, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 0), (2, 0)]
        ]),
        # Back L
        gm.TetrisPiece([
            [(0, 0), (1, 0), (2, 0), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (0, 2)],
            [(0, 0), (1, 0), (0, 1), (0, 2)],
            [(0, 0), (0, 1), (1, 1), (2, 1)]
        ]),
        # Square
        gm.TetrisPiece([
            [(0, 0), (0, 1), (1, 0), (1, 1)],
        ]),
        # Left Chair
        gm.TetrisPiece([
            [(1, 0), (1, 1), (0, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (2, 1)]
        ]),
        # T
        gm.TetrisPiece([
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(1, 0), (1, 1), (0, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (0, 1)]
        ]),
        # Right Chair
        gm.TetrisPiece([
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 0), (2, 0)]
        ])
    ])

    tetris.currentState = state


    while not displayManager.isWindowClosed():
        print("Printing states")
        for piece in tetris.pieces:
            nextStates = tetris.possibleStates(piece)
            for state in nextStates:
                displayManager.displayState(state)
                time.sleep(0.2)





