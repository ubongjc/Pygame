import pygame
import constants


class UserPlayer(pygame.sprite.Sprite):
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

    def is_valid_move(self, cell_x, cell_y):
        if len(self.path) == 0:
            return True
        last_cell = self.path[-1]
        dx = abs(last_cell[0] - cell_x)
        dy = abs(last_cell[1] - cell_y)
        return (dx == 1 and dy == 0) or (dx == 0 and dy == 1)

    def shoot_bullet(self, direction, current_path_index=-1):
        if self.fired_bullets.count(True) >= constants.MAX_BULLETS:
            return

        start_pos = self.path[current_path_index - 1]
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

    def update_user_bullets(self, computer_player, play_index):
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
                return False
            elif play_index < len(computer_player.path):
                if self.check_user_bullet_collision(computer_player.path[play_index][0],
                                                    computer_player.path[play_index][1]):
                    return True

            if self.bullet_at_position(computer_player, bullet['x'], bullet['y']):
                self.bullets.remove(bullet)
                return False
            elif play_index < len(computer_player.path):
                if self.check_user_bullet_collision(computer_player.path[play_index][0],
                                                    computer_player.path[play_index][1]):
                    return True

    def check_user_bullet_collision(self, x, y):
        for bullet in self.bullets:
            if bullet['x'] == x and bullet['y'] == y:
                return True
        return False

    def bullet_at_position(self, computer_player, x, y):
        for bullet in computer_player.bullets:
            if bullet['x'] == x and bullet['y'] == y:
                return True
        return False
