class Table:
    pixels: list

    def __init__(self, pixels):
        self.pixels = pixels

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
        return BoardProperties(
            holes=self.table.getNumberOfHoles(),
            fullLines=self.table.fullLines(),
            bumpiness=self.table.bumpiness(),
            totalHeight=self.table.totalHeight()
        )


class BoardProperties:

    holes: int
    fullLines: int
    bumpiness: int
    totalHeight: int

    def __init__(self, holes: int, fullLines: int, bumpiness: int, totalHeight: int):
        self.holes = holes
        self.fullLines = fullLines
        self.bumpiness = bumpiness
        self.totalHeight = totalHeight
