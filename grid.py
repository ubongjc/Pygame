import pygame
import constants


class Grid:
    def __init__(self, size, user_player, user_player2, computer_player):
        self.size = size
        self.grid = [[[0, 0] for _ in range(size)] for _ in range(size)]
        self.game_over = False
        self.winner = None
        self.background_image = pygame.image.load("images/background.png")
        self.scaled_background = pygame.transform.scale(self.background_image,
                                                        (constants.SCREEN_SIZE, constants.SCREEN_SIZE))
        self.player = user_player
        self.player2 = user_player2
        self.computer_player = computer_player

    def draw(self, surface, show_lines=True, current_path_index=None):
        if self.winner:
            self.display_result_text(surface)
        else:
            # surface.blit(self.scaled_background, (0, 0))
            surface.fill(constants.WHITE)
            self.draw_grid_cells(surface, show_lines)
            self.update_player1_position(current_path_index)
            self.update_player2_position(current_path_index)
            self.update_computer_player_position(current_path_index)
            self.draw_players(surface)
            bullet_radius = constants.CELL_SIZE // 8
            self.draw_player1_bullets(surface, bullet_radius)
            self.draw_player2_bullets(surface, bullet_radius)
            self.draw_computer_player_bullets(surface, bullet_radius)

    def draw_highlight(self, surface):
        if self.player2:
            last_cell = self.player2.path[-1]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = last_cell[0] + dx, last_cell[1] + dy
                if 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x][1] == 0:
                    pygame.draw.rect(surface, constants.BLUE, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                               constants.CELL_SIZE, constants.CELL_SIZE), 1)
        else:
            last_cell = self.player.path[-1]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = last_cell[0] + dx, last_cell[1] + dy
                if 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x][0] == 0:
                    pygame.draw.rect(surface, constants.RED, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                              constants.CELL_SIZE, constants.CELL_SIZE), 1)

    def update_bullets(self, play_index):
        if self.winner is None:
            self.game_over = self.player.update_user_bullets(self.computer_player, self.player2, play_index - 1)
            if self.game_over:
                self.winner = "Player 1"

        if self.winner is None and self.player2:
            self.game_over = self.player2.update_user_bullets(self.computer_player, self.player, play_index - 1)
            if self.game_over:
                self.winner = "Player 2"

        if self.winner is None and self.computer_player and not self.player2:
            self.game_over = self.computer_player.update_bullets_computer(self.player, play_index - 1)
            if self.game_over:
                self.winner = "Computer"

    def display_result_text(self, surface):
        result_font = pygame.font.Font(None, 50)
        result_text = None
        if self.winner == "Player 1":
            result_text = result_font.render("Player 1 Wins!", True, constants.BLACK)
        elif self.winner == "Player 2":
            result_text = result_font.render("Player 2 Wins!", True, constants.BLACK)
        elif self.winner == "computer":
            result_text = result_font.render("Game Over", True, constants.BLACK)
        text_rect = result_text.get_rect(center=(constants.SCREEN_SIZE // 2, constants.SCREEN_SIZE // 2))
        surface.blit(result_text, text_rect)

    def draw_grid_cells(self, surface, show_lines):
        for y in range(self.size):
            for x in range(self.size):
                color = None
                if self.grid[y][x][0] == 1:
                    if (x, y) == self.player.path[-1]:
                        color = (136, 8, 8)  # Slightly different shade of red
                    else:
                        color = constants.RED

                if self.grid[y][x][1] == 1:
                    if (x, y) == self.player2.path[-1]:
                        color = (0, 0, 139)  # Slightly different shade of blue
                    else:
                        color = constants.BLUE

                if color:
                    pygame.draw.rect(surface, color, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                      constants.CELL_SIZE, constants.CELL_SIZE))
                if show_lines:
                    pygame.draw.rect(surface, constants.GREY, (x * constants.CELL_SIZE, y * constants.CELL_SIZE,
                                                               constants.CELL_SIZE, constants.CELL_SIZE), 1)

    def update_player1_position(self, current_path_index):
        if current_path_index is not None and 0 <= current_path_index < len(self.player.path):
            self.player.rect.x = self.player.path[current_path_index][0] * constants.CELL_SIZE
            self.player.rect.y = self.player.path[current_path_index][1] * constants.CELL_SIZE

    def update_player2_position(self, current_path_index):
        if self.player2 and current_path_index is not None and 0 <= current_path_index < len(self.player2.path):
            self.player2.rect.x = self.player2.path[current_path_index][0] * constants.CELL_SIZE
            self.player2.rect.y = self.player2.path[current_path_index][1] * constants.CELL_SIZE

    def update_computer_player_position(self, current_path_index):
        if self.computer_player and not self.player2 and current_path_index is not None and \
                0 <= current_path_index < len(self.computer_player.path):
            self.computer_player.rect.x = self.computer_player.path[current_path_index][0] * constants.CELL_SIZE
            self.computer_player.rect.y = self.computer_player.path[current_path_index][1] * constants.CELL_SIZE

    def draw_players(self, surface):
        if self.player.rect.x > -1 and self.player.rect.y > -1:
            surface.blit(self.player.image, self.player.rect)
        if self.player2 and self.player2.rect.x > -1 and self.player2.rect.y > -1:
            surface.blit(self.player2.image, self.player2.rect)
        if self.computer_player and self.computer_player.rect.x > -1 and self.computer_player.rect.y > -1:
            surface.blit(self.computer_player.image, self.computer_player.rect)

    def draw_player1_bullets(self, surface, bullet_radius):
        for bullet in self.player.bullets:
            pygame.draw.circle(surface, constants.RED,
                               (bullet['x'] * constants.CELL_SIZE + constants.CELL_SIZE // 2,
                                bullet['y'] * constants.CELL_SIZE + constants.CELL_SIZE // 2),
                               bullet_radius)

    def draw_player2_bullets(self, surface, bullet_radius):
        if self.player2:
            for bullet in self.player2.bullets:
                pygame.draw.circle(surface, constants.BLUE,
                                   (bullet['x'] * constants.CELL_SIZE + constants.CELL_SIZE // 2,
                                    bullet['y'] * constants.CELL_SIZE + constants.CELL_SIZE // 2),
                                   bullet_radius)

    def draw_computer_player_bullets(self, surface, bullet_radius):
        if self.computer_player and not self.player2:
            for bullet in self.computer_player.bullets:
                pygame.draw.circle(surface, constants.BLUE,
                                   (bullet['x'] * constants.CELL_SIZE + constants.CELL_SIZE // 2,
                                    bullet['y'] * constants.CELL_SIZE + constants.CELL_SIZE // 2),
                                   bullet_radius)
