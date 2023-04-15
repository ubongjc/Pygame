import math
import random
import pygame
import constants


class ComputerPlayer(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scaled_background = pygame.transform.scale(self.image,
                                                        (constants.GRID_SIZE, constants.GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * constants.CELL_SIZE
        self.rect.y = y * constants.CELL_SIZE
        self.bullets = []
        self.path = []
        self.fired_bullets = [False] * constants.MAX_BULLETS
        self.start_random_position()
        self.generate_path()

    def start_random_position(self):
        x, y = random.randint(0, constants.GRID_SIZE - 1), random.randint(0, constants.GRID_SIZE - 1)
        self.path.append((x, y))

    def valid_moves(self, current_pos):
        valid_moves = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = current_pos[0] + dx, current_pos[1] + dy
            if 0 <= x < constants.GRID_SIZE and 0 <= y < constants.GRID_SIZE:
                #  and self.grid.grid[y][x] == 0
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

    def shoot_bullet_computer(self, direction, current_path_index=-1):
        if self.fired_bullets.count(True) >= constants.MAX_BULLETS:
            return

        shooter_x = self.path[current_path_index - 1][0]
        shooter_y = self.path[current_path_index - 1][1]
        start_pos = (shooter_x, shooter_y)
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

    def update_bullets_computer(self, player, play_index):
        for bullet in self.bullets:
            if bullet['direction'] == 'left':
                bullet['x'] -= 1
            elif bullet['direction'] == 'right':
                bullet['x'] += 1
            elif bullet['direction'] == 'up':
                bullet['y'] -= 1
            elif bullet['direction'] == 'down':
                bullet['y'] += 1

            if bullet['x'] < 0 or bullet['x'] >= constants.GRID_SIZE or bullet['y'] < 0 or \
                    bullet['y'] >= constants.GRID_SIZE:
                self.bullets.remove(bullet)
            elif play_index < len(player.path):
                if self.check_computer_bullet_collision(player.path[play_index][0], player.path[play_index][1]):
                    return True

            if self.bullet_at_position(player, bullet['x'], bullet['y']):
                self.bullets.remove(bullet)
            elif play_index < len(player.path):
                if self.check_computer_bullet_collision(player.path[play_index][0], player.path[play_index][1]):
                    return True

    def get_direction_towards_user(self, user_path, x, y):
        if not user_path:
            return random.choice(['left', 'right', 'up', 'down'])

        target_x, target_y = user_path[-1]  # Get the user's current position
        dx, dy = target_x - x, target_y - y

        angle = math.degrees(math.atan2(dy, dx))  # Calculate the angle in degrees
        angle = (angle + 360) % 360  # Normalize angle to the range [0, 360)

        # Define directions and their corresponding angles
        directions_angles = {
            'right': 0,
            'down': 90,
            'left': 180,
            'up': 270
        }

        # Find the closest direction to the calculated angle
        closest_direction = min(directions_angles, key=lambda direction: abs(directions_angles[direction] - angle))

        return closest_direction

    def check_computer_bullet_collision(self, x, y):
        for bullet in self.bullets:
            if bullet['x'] == x and bullet['y'] == y:
                return True
        return False

    def bullet_at_position(self, player, x, y):
        for bullet in player.bullets:
            if bullet['x'] == x and bullet['y'] == y:
                return True
        return False
