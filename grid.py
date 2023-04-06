import pygame
from constants import *


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.path = []
        self.bullets = []
        self.firedBullets = []
        self.bullet_start_indices = []

    def draw(self, surface, show_lines=True, current_path_index=None, computer_path=None):
        surface.fill(WHITE)
        for y in range(self.size):
            for x in range(self.size):
                if current_path_index is not None and (x, y) == self.path[current_path_index]:
                    color = RED
                elif self.grid[y][x] == 1:
                    if (x, y) == self.path[-1]:
                        color = (136, 8, 8)  # Slightly different shade of red
                    else:
                        color = RED
                else:
                    color = None

                if color:
                    pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                if show_lines:
                    pygame.draw.rect(surface, GREY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        for y in range(self.size):
            for x in range(self.size):
                color = None
                if current_path_index is not None \
                        and computer_path is not None \
                        and (x, y) == computer_path[current_path_index]:
                    color = BLUE

                if color:
                    pygame.draw.rect(surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for bullet in self.bullets:
            pygame.draw.rect(surface, BLACK, (bullet['x'] * CELL_SIZE, bullet['y'] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def is_valid_move(self, cell_x, cell_y):
        if len(self.path) == 0:
            return True
        last_cell = self.path[-1]
        dx = abs(last_cell[0] - cell_x)
        dy = abs(last_cell[1] - cell_y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def draw_highlight(self, surface, cell_x, cell_y):
        last_cell = self.path[-1]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = last_cell[0] + dx, last_cell[1] + dy
            if 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x] == 0:
                pygame.draw.rect(surface, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def shoot_bullet(self, direction, start_pos=None, current_path_index=-1):
        if start_pos is None:
            start_pos = self.path[-1] if self.path else (0, 0)

        bullet = {
            'x': start_pos[0],
            'y': start_pos[1],
            'direction': direction
        }
        self.bullets.append(bullet)

        if current_path_index != -1:
            self.firedBullets[current_path_index - 1] = True

    def update_bullets(self):
        for bullet in self.bullets:
            if bullet['direction'] == 'left':
                bullet['x'] -= 1
            elif bullet['direction'] == 'right':
                bullet['x'] += 1
            elif bullet['direction'] == 'up':
                bullet['y'] -= 1
            elif bullet['direction'] == 'down':
                bullet['y'] += 1

            if bullet['x'] < 0 or bullet['x'] >= self.size or bullet['y'] < 0 or bullet['y'] >= self.size:
                self.bullets.remove(bullet)

    def get_direction_towards_user(self, bullet_x, bullet_y, user_position=None):
        if user_position is None:
            user_position = self.path[-1] if self.path else (0, 0)

        dx = user_position[0] - bullet_x
        dy = user_position[1] - bullet_y

        if abs(dx) > abs(dy):
            return 'right' if dx > 0 else 'left'
        else:
            return 'down' if dy > 0 else 'up'
