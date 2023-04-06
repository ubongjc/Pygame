import random


class ComputerPlayer:
    def __init__(self, grid):
        self.grid = grid
        self.path = []
        self.fired_bullets = []
        self.start_random_position()

    def start_random_position(self):
        x, y = random.randint(0, self.grid.size - 1), random.randint(0, self.grid.size - 1)
        self.path.append((x, y))

    def valid_moves(self):
        valid_moves = []
        if len(self.path) > 0:
            last_cell = self.path[-1]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = last_cell[0] + dx, last_cell[1] + dy
                if 0 <= x < self.grid.size and 0 <= y < self.grid.size and self.grid.grid[y][x] == 0:
                    if(x, y) not in self.path:
                        valid_moves.append((x, y))
        return valid_moves

    def choose_random_move(self):
        moves = self.valid_moves()
        if moves:
            self.path.append(random.choice(moves))
            self.fired_bullets.append(False)

    def rollback_to_validity_if_necessary(self):
        print(f'original self.path => {self.path}')
        num_valid = len(self.valid_moves())
        popped_value = (-1, -1)
        if num_valid < 1 and len(self.path) > 0:
            while num_valid < 2 and len(self.path) > 0:
                popped_value = self.path.pop()
                print(f'popped_value => {popped_value}')
                num_valid = len(self.valid_moves())
                print(f'num_valid => {num_valid}')
            temp = self.valid_moves()
            if popped_value in temp:
                temp.remove(popped_value)
                print(f'temp => {temp}')
            if len(temp) > 0:
                self.path.append(temp[0])
                print(f'self.path => {self.path}')
            return True
        return False
