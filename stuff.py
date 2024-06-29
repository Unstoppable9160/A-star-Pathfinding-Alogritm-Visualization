import pygame

BACKGROUND = (17, 16, 26)

START = (255, 150, 82)
END = (88, 81, 213)
WALL = (255, 255, 255)

FINAL_PATH_COLOUR = (232, 44, 23)
SCANNED_AREA = (89, 101, 111)
BORDER_THINGY = (47, 46, 63)

GRID_BORDERS = (0, 0, 0)



class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BACKGROUND
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == SCANNED_AREA

    def is_open(self):
        return self.color == BORDER_THINGY

    def is_barrier(self):
        return self.color == WALL

    def is_start(self):
        return self.color == START

    def is_end(self):
        return self.color == END

    def reset(self):
        self.color = BACKGROUND

    def make_start(self):
        self.color = START

    def make_closed(self):
        self.color = SCANNED_AREA

    def make_open(self):
        self.color = BORDER_THINGY

    def make_barrier(self):
        self.color = WALL

    def make_end(self):
        self.color = END

    def make_path(self):
        self.color = FINAL_PATH_COLOUR

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False