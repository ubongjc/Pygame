import pygame

import constants


class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.path = []
        self.bullets = []
        self.fired_bullets = []
        self.computer_bullets = []
        self.bullet_start_indices = []
        self.game_over = False
        self.winner = None

    def draw(self, surface, show_lines=True, current_path_index=None, computer_path=None):
        if self.winner:
            result_font = pygame.font.Font(None, 50)
            result_text = None
            if self.winner == "user":
                result_text = result_font.render("You Win!", True, constants.BLACK)
            elif self.winner == "computer":
                result_text = result_font.render("Game Over", True, constants.BLACK)
            text_rect = result_text.get_rect(center=(constants.SCREEN_SIZE // 2, constants.SCREEN_SIZE // 2))
            surface.blit(result_text, text_rect)
        else:
            surface.fill(constants.WHITE)
            for y in range(self.size):
                for x in range(self.size):
                    if current_path_index is not None and \
                            0 <= current_path_index < len(self.path) and \
                            (x, y) == self.path[current_path_index]:
                        color = constants.RED
                    elif self.grid[y][x] == 1:
                        if (x, y) == self.path[-1]:
                            color = (136, 8, 8)  # Slightly different shade of red
                        else:
                            color = constants.RED
                    else:
                        color = None

                    if color:
                        pygame.draw.rect(surface, color, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                          constants.CELL_SIZE, constants.CELL_SIZE))

                    if show_lines:
                        pygame.draw.rect(surface, constants.GREY, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                                   constants.CELL_SIZE, constants.CELL_SIZE), 1)

            for y in range(self.size):
                for x in range(self.size):
                    if current_path_index is not None and \
                            current_path_index < len(computer_path) and \
                            computer_path is not None:
                        color = None
                        if (x, y) == computer_path[current_path_index]:
                            color = constants.BLUE

                        if color:
                            pygame.draw.rect(surface, color, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                              constants.CELL_SIZE, constants.CELL_SIZE))

            bullet_radius = constants.CELL_SIZE // 8  # Adjust this value to change the bullet size

            for bullet in self.bullets:
                pygame.draw.circle(surface, constants.RED,
                                   (bullet['x'] * constants.CELL_SIZE + constants.CELL_SIZE // 2,
                                    bullet['y'] * constants.CELL_SIZE + constants.CELL_SIZE // 2),
                                   bullet_radius)

            for bullet in self.computer_bullets:
                pygame.draw.circle(surface, constants.BLUE,
                                   (bullet['x'] * constants.CELL_SIZE + constants.CELL_SIZE // 2,
                                    bullet['y'] * constants.CELL_SIZE + constants.CELL_SIZE // 2),
                                   bullet_radius)

    def is_valid_move(self, cell_x, cell_y):
        if len(self.path) == 0:
            return True
        last_cell = self.path[-1]
        dx = abs(last_cell[0] - cell_x)
        dy = abs(last_cell[1] - cell_y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def draw_highlight(self, surface):
        last_cell = self.path[-1]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = last_cell[0] + dx, last_cell[1] + dy
            if 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x] == 0:
                pygame.draw.rect(surface, constants.RED, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                          constants.CELL_SIZE, constants.CELL_SIZE), 1)

    def shoot_bullet(self, direction, start_pos=None, current_path_index=-1):
        if self.winner is None:
            if self.fired_bullets.count(True) >= constants.MAX_BULLETS:
                return

            if start_pos is None:
                start_pos = self.path[-1] if self.path else (0, 0)

            bullet = {
                'x': start_pos[0],
                'y': start_pos[1],
                'direction': direction
            }
            self.bullets.append(bullet)

            if current_path_index != -1:
                self.fired_bullets[current_path_index - 1] = True

    def shoot_bullet_computer(self, direction, start_pos=None, current_path_index=-1, computer_player=None):
        if self.winner is None:
            if computer_player.fired_bullets.count(True) >= constants.MAX_BULLETS:
                return

            if start_pos is None:
                start_pos = computer_player.path[-1] if computer_player.path else (0, 0)

            bullet = {
                'x': start_pos[0],
                'y': start_pos[1],
                'direction': direction
            }
            self.computer_bullets.append(bullet)

            if current_path_index != -1:
                computer_player.fired_bullets[current_path_index - 1] = True

    def update_bullets(self, computer_path, play_index):
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
            elif self.check_user_bullet_collision(computer_path[play_index][0], computer_path[play_index][1]):
                self.winner = "user"
                self.game_over = True

    def update_bullets_computer(self, user_path, play_index):
        for bullet in self.computer_bullets:
            if bullet['direction'] == 'left':
                bullet['x'] -= 1
            elif bullet['direction'] == 'right':
                bullet['x'] += 1
            elif bullet['direction'] == 'up':
                bullet['y'] -= 1
            elif bullet['direction'] == 'down':
                bullet['y'] += 1

            if bullet['x'] < 0 or bullet['x'] >= self.size or bullet['y'] < 0 or bullet['y'] >= self.size:
                self.computer_bullets.remove(bullet)
            elif self.check_computer_bullet_collision(user_path[play_index][0], user_path[play_index][1]):
                self.winner = "computer"
                self.game_over = True

    def get_direction_towards_user(self, bullet_x, bullet_y, user_position=None):
        if user_position is None:
            user_position = self.path[-1] if self.path else (0, 0)

        dx = user_position[0] - bullet_x
        dy = user_position[1] - bullet_y

        if abs(dx) > abs(dy):
            return 'right' if dx > 0 else 'left'
        else:
            return 'down' if dy > 0 else 'up'

    def check_user_bullet_collision(self, x, y):
        for bullet in self.bullets:
            if bullet['x'] == x and bullet['y'] == y:
                return True
        return False

    def check_computer_bullet_collision(self, x, y):
        for bullet in self.computer_bullets:
            if bullet['x'] == x and bullet['y'] == y:
                return True
        return False
