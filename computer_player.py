import random
import constants


class ComputerPlayer:
    def __init__(self, grid):
        self.grid = grid
        self.path = []
        self.fired_bullets = []
        self.start_random_position()
        self.generate_path()

    def start_random_position(self):
        x, y = random.randint(0, self.grid.size - 1), random.randint(0, self.grid.size - 1)
        self.path.append((x, y))

    def valid_moves(self, current_pos):
        valid_moves = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = current_pos[0] + dx, current_pos[1] + dy
            if 0 <= x < self.grid.size and 0 <= y < self.grid.size and self.grid.grid[y][x] == 0:
                if (x, y) not in self.path:
                    valid_moves.append((x, y))
        return valid_moves

    def generate_path(self):
        def backtrack(current_pos):
            if len(self.path) >= constants.MAX_MOVES:
                return True

            moves = self.valid_moves(current_pos)
            random.shuffle(moves)
            for move in moves:
                self.path.append(move)
                self.fired_bullets.append(False)
                if backtrack(move):
                    return True
                self.path.pop()
                self.fired_bullets.pop()
            return False

        while True:
            success = backtrack(self.path[0])
            if success and len(self.path) == constants.MAX_MOVES:
                break
            self.path = [self.path[0]]
            self.fired_bullets = []
