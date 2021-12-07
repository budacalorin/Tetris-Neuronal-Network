class Table:
    pixels: list

    def __init__(self, pixels):
        self.pixels = pixels


class State:

    table: Table

    def __init__(self, table: Table):
        self.table = table
