import GameModule as gm
import Deep_Learning_Agent as dqa
import time
displaying = True
if displaying:
    import DisplayModule as dm

if __name__ == '__main__':
    if displaying:
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

    if displaying:
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

    episodes = 2000
    maxSteps = 500
    epsilonStopEpisode = 1500
    memSize = 20000
    discount = 0.95
    batchSize = 1000
    epochs = 1
    renderEvery = 50
    logEvery = 50
    replayStart_Size = 2000
    trainEvery = 32
    nNeurons = [32, 32]
    renderDelay = None
    activations = ['relu', 'relu', 'linear']
    saveEvery = 200

    agent = dqa.DeepLearningAgent(4, "model_agent.h5")

    bestGame = []
    maxScore = 0

    for episode in range(episodes):
        tetris.restart()
        currentState = tetris.currentState
        done = False
        steps = 0

        # Game
        print(f"Started {episode}")

        nextStates = tetris.getNextStates()

        states = []

        while not done and (not maxSteps or steps < maxSteps):
            if displaying:
                displayManager.isWindowClosed()

            nextStatesProperties = list(map(lambda s: s.getStateProperties(), nextStates))


            best_state_index = agent.best_state(nextStatesProperties)
            best_state = nextStates[best_state_index]
            best_state_properties = nextStatesProperties[best_state_index]

            states.append(best_state)

            old_state = tetris.currentState

            reward, done = tetris.play(best_state)

            nextStates = tetris.getNextStates()

            if len(nextStates) == 0:
                done = True

            agent.add_to_memory(best_state_properties, old_state.getStateProperties(), reward, done)
            steps += 1

        print(f"Finished with score {tetris.score}")
        # print(tetris.currentState.table.pixels)

        if tetris.score > maxScore:
            maxScore = tetris.score
            bestGame = states

        # Train
        if episode % trainEvery == 0:
            agent.train(batch_size=batchSize, epochs=epochs)

        if episode % saveEvery == 0:
            agent.model.save("model_agent.h5")

        if episode % renderEvery == 0:
            print(maxScore)
            maxScore = 0
            for state in bestGame:
                displayManager.displayState(state)
                time.sleep(0.1)
