import random


class Table:
    pixels: list

    def __init__(self, pixels):
        self.pixels = pixels

    def clone(self):
        return Table(
            pixels= [x[:] for x in self.pixels]
        )

    def getMaxHeights(self):
        numberOfLines = len(self.pixels)
        maxHeights = [0 for _ in range(len(self.pixels[0]))]
        for lineIndex in range(len(self.pixels)):
            line = self.pixels[lineIndex]

            for columnIndex in range(len(line)):
                if maxHeights[columnIndex] == 0 and line[columnIndex] != 0:
                    maxHeights[columnIndex] = numberOfLines - lineIndex

        return maxHeights

    def getNumberOfHoles(self):
        maxHeights = self.getMaxHeights()
        holes = 0
        numberOfLines = len(self.pixels)

        for columnIndex in range(len(self.pixels[0])):
            for rowIndex in range(numberOfLines - maxHeights[columnIndex], numberOfLines):
                if self.pixels[rowIndex][columnIndex] == 0:
                    holes += 1

        return holes

    def fullLines(self):
        return sum(
            map(
                lambda line: all(map(lambda pixel: pixel != 0, line)),
                self.pixels
            )
        )

    def bumpiness(self):
        bumpiness = 0
        maxHeights = self.getMaxHeights()
        for columnIndex in range(len(maxHeights) - 1):
            bumpiness += abs(maxHeights[columnIndex] - maxHeights[columnIndex + 1])

        return bumpiness

    def totalHeight(self):
        return sum(self.getMaxHeights())


class State:

    table: Table

    def __init__(self, table: Table):
        self.table = table

    def getStateProperties(self):
        return StateProperties(
            holes=self.table.getNumberOfHoles(),
            fullLines=self.table.fullLines(),
            bumpiness=self.table.bumpiness(),
            totalHeight=self.table.totalHeight()
        )

    def clone(self):
        return State(
            table=self.table.clone()
        )


class StateProperties:

    holes: int
    fullLines: int
    bumpiness: int
    totalHeight: int

    def __init__(self, holes: int, fullLines: int, bumpiness: int, totalHeight: int):
        self.holes = holes
        self.fullLines = fullLines
        self.bumpiness = bumpiness
        self.totalHeight = totalHeight


class TetrisPiece:

    possiblePositions: list

    def __init__(self, allPositions: list):
        self.possiblePositions = allPositions


class TetrisHelper:

    pieces: list
    currentState: State
    score: int

    def __init__(self, pieces: list):
        self.pieces = pieces
        self.restart()

    def restart(self):
        self.currentState = self.getInitialPosition()
        self.score = 0

    def getInitialPosition(self) -> State:
        return State(Table(
            [[0 for _ in range(10)] for _ in range(15)]
        ))

    def simulateDrop(self, piecePosition: list, column) -> State:
        lowest = -1
        found = False

        while lowest < 15 and not found:
            lowest += 1
            found = self.collision(column, lowest, piecePosition)

        if lowest == 0:
            print("Could not place piece")
            return self.currentState.clone()
        lowest -= 1

        clone = self.currentState.clone()
        self.placePiece(clone, column, lowest, piecePosition)

        return clone

    def placePiece(self, state: State, column: int, lowest: int, piecePosition: list):
        color = random.randint(0, 6) + 1
        for piecePosition in piecePosition:
            x = lowest + piecePosition[0]
            y = column + piecePosition[1]
            state.table.pixels[x][y] = color

    def collision(self, column: int, line: int, piecePositions: list) -> bool:
        for piecePosition in piecePositions:
            x = line + piecePosition[0]
            y = column + piecePosition[1]
            if x >= 15 or y >= 10:
                return True
            if self.currentState.table.pixels[x][y] != 0:
                return True

        return False

    def possibleStates(self, piece: TetrisPiece) -> list:
        states = []
        for column in range(10):
            for piecePosition in piece.possiblePositions:
                if not self.collision(column, 0, piecePosition):
                    states.append(self.simulateDrop(piecePosition, column))

        return states

    def getNextStates(self) -> list:
        nextPiece = random.randint(0, len(self.pieces) - 1)
        return self.possibleStates(self.pieces[nextPiece])

    def extractReward(self, state) -> (State, int):
        extractedTable = Table([])
        fullLines = 0
        placedPieces = 0

        for line in state.table.pixels:
            pixels = sum(map(lambda pixel: pixel != 0, line))
            placedPieces += pixels

            if pixels != 10:
                extractedTable.pixels.append(line)
            else:
                fullLines += 1

        while len(extractedTable.pixels) != 15:
            extractedTable.pixels.insert(0, [0 for _ in range(10)])

        return State(extractedTable), 1 + fullLines ^ 2 * 10 #+ placedPieces

    def play(self, state: State):
        self.currentState, reward = self.extractReward(state)
        self.score += reward
        return reward, False


