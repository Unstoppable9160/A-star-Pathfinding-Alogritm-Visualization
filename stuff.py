import time
import pygame
import threading

BACKGROUND = (17, 16, 26)

START = (255, 150, 82)
END = (88, 81, 213)
WALL = (255, 255, 255)

FINAL_PATH_COLOUR = (232, 44, 23)
SCANNED_AREA = (89, 101, 111)
BORDER_THINGY = (47, 46, 63)

GRID_BORDERS = (0, 0, 0)



class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self._thread = None

    def _run(self):
        while self.running:
            time.sleep(0.01)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
            self._thread.join()

    def reset(self):
        self.stop()
        self.start_time = None
        self.elapsed_time = 0

    def get_elapsed_time(self):
        if self.running:
            elapsed_time_secs = time.time() - self.start_time
        else:
            elapsed_time_secs = self.elapsed_time
        
        minutes = int(elapsed_time_secs // 60)
        seconds = int(elapsed_time_secs % 60)
        milliseconds = int((elapsed_time_secs - int(elapsed_time_secs)) * 1000)

        return f"{minutes} minute(s) {seconds} second(s) {milliseconds} millisecond(s)"


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