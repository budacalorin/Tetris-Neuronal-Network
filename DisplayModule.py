import pygame
import GameModule


class Size:
    width: int
    height: int

    def __init__(self, width, height):
        self.width = width
        self.height = height


class Padding:
    left: int
    right: int
    up: int
    down: int

    def __init__(self, left: int, right: int, up: int, down: int):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


class DisplayManager:
    PIECE_SIZE = Size(20, 20)
    MATRIX_SEPARATORS_IN_PIXELS = 1
    TABLE_PADDING_IN_PIXELS = Padding(15, 15, 30, 5)
    NUMBER_OF_COLUMNS = 10
    NUMBER_OF_ROWS = 15
    COLORS = [
        pygame.color.Color("#000000"),
        pygame.color.Color("#ffff00"),
        pygame.color.Color("#03ff00"),
        pygame.color.Color("#ff0000"),
        pygame.color.Color("#0000ab"),
        pygame.color.Color("#ff7800"),
        pygame.color.Color("#03ffff"),
    ]

    screen: pygame.Surface

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TETRIS")

        displaySize = self.getDisplaySize()
        self.screen = pygame.display.set_mode((displaySize.width, displaySize.height))

    def getDisplaySize(self) -> Size:
        return Size(
            width=self.TABLE_PADDING_IN_PIXELS.left + self.TABLE_PADDING_IN_PIXELS.right + self.NUMBER_OF_COLUMNS * (
                        self.PIECE_SIZE.width + self.MATRIX_SEPARATORS_IN_PIXELS) - self.MATRIX_SEPARATORS_IN_PIXELS,
            height=self.TABLE_PADDING_IN_PIXELS.up + self.TABLE_PADDING_IN_PIXELS.down + self.NUMBER_OF_ROWS * (
                        self.PIECE_SIZE.height + self.MATRIX_SEPARATORS_IN_PIXELS) - self.MATRIX_SEPARATORS_IN_PIXELS
        )

    def getColor(self, forColorIndex: int) -> pygame.Color:
        if forColorIndex == 0:
            return self.COLORS[0]

        # This is to not display the 0th color, as it is black
        return self.COLORS[forColorIndex % (len(self.COLORS) - 1) + 1]

    def displayPiece(self, row: int, column: int, colorIndex: int):
        pygame.draw.rect(self.screen, self.getColor(colorIndex), self.getPieceRect(row, column))

    def getPieceRect(self, row: int, column: int) -> pygame.Rect:
        return pygame.Rect(
            self.getPxForColumn(column),
            self.getPxForRow(row),
            self.PIECE_SIZE.width,
            self.PIECE_SIZE.height
        )

    def getPxForColumn(self, columnIndex: int) -> int:
        return self.TABLE_PADDING_IN_PIXELS.left + \
               columnIndex * (self.PIECE_SIZE.width + self.MATRIX_SEPARATORS_IN_PIXELS) - \
               self.MATRIX_SEPARATORS_IN_PIXELS

    def getPxForRow(self, rowIndex: int) -> int:
        return self.TABLE_PADDING_IN_PIXELS.down + \
               (rowIndex + 1) * (self.PIECE_SIZE.height + self.MATRIX_SEPARATORS_IN_PIXELS) - \
               self.MATRIX_SEPARATORS_IN_PIXELS

    def clearDisplay(self):
        self.screen.fill(self.COLORS[0])

    def displayState(self, state: GameModule.State):
        self.clearDisplay()

        for rowIndex in range(0, self.NUMBER_OF_ROWS):
            for columnIndex in range(0, self.NUMBER_OF_COLUMNS):
                self.displayPiece(rowIndex, columnIndex, state.table.pixels[rowIndex][columnIndex])

        pygame.display.update()

    def isWindowClosed(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False
