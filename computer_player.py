import random


class ComputerPlayer:
    def __init__(self, grid):
        self.grid = grid
        self.path = []
        self.start_random_position()

    def start_random_position(self):
        x, y = random.randint(0, self.grid.size - 1), random.randint(0, self.grid.size - 1)
        self.path.append((x, y))

    def valid_moves(self):
        valid_moves = []
        last_cell = self.path[-1]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = last_cell[0] + dx, last_cell[1] + dy
            if 0 <= x < self.grid.size and 0 <= y < self.grid.size and self.grid.grid[y][x] == 0:
                valid_moves.append((x, y))
        return valid_moves

    def choose_random_move(self):
        moves = self.valid_moves()
        if moves:
            self.path.append(random.choice(moves))
