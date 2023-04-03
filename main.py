import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
SCREEN_SIZE = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Button:
    def __init__(self, x, y, width, height, text, color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font_size = font_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text, text_rect)

    def is_clicked(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


# Grid class
class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.path = []
        self.bullets = []
        self.firedBullets = []
        self.bullet_start_indices = []

    def draw(self, surface, show_lines=True, current_path_index=None):
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
            self.firedBullets[current_path_index-1] = True

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


# Main function
def main():
    global CELL_SIZE, SCREEN_SIZE

    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Grid Game")
    clock = pygame.time.Clock()
    BULLET_UPDATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BULLET_UPDATE_EVENT, 500)  # Set the interval to 500ms

    grid = Grid(GRID_SIZE)
    grid.bullet_start_indices = []
    show_lines = True
    play_button = Button(10, 10, 100, 40, "Play", (0, 128, 0), 30)

    play_mode = False
    play_index = 0
    play_timer = 0
    play_interval = 1000  # Time interval in milliseconds between path cells

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == BULLET_UPDATE_EVENT:
                grid.update_bullets()

            # Input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse coordinates
                x, y = pygame.mouse.get_pos()

                # Check if the play button is clicked
                if play_button.is_clicked(x, y):
                    print("User's selected path:", grid.path)  # Print the user's selected path
                    show_lines = False
                    grid.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    play_mode = True
                    play_index = 0
                    play_timer = pygame.time.get_ticks()

                if not play_mode:
                    # Get cell coordinates
                    cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE

                    # Toggle cell color
                    if grid.is_valid_move(cell_x, cell_y) and grid.grid[cell_y][cell_x] == 0:
                        grid.grid[cell_y][cell_x] = 1
                        grid.path.append((cell_x, cell_y))
                        grid.firedBullets.append(False)
                    elif grid.path and (cell_x, cell_y) == grid.path[-1]:
                        grid.grid[cell_y][cell_x] = 0
                        grid.path.pop()
                        grid.firedBullets.pop()

            # Shoot bullet
            if event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'

                if direction:
                    if \
                        play_mode and \
                        play_index > 0 and \
                        grid.firedBullets[play_index - 1] is False:
                        grid.shoot_bullet(direction, grid.path[play_index - 1], play_index)
                    elif not play_mode:
                        grid.shoot_bullet(direction)

            # Toggle grid lines
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_lines = not show_lines

            # Resize the screen
            if event.type == pygame.VIDEORESIZE:
                width, height = event.w, event.h
                CELL_SIZE = min(width // GRID_SIZE, height // GRID_SIZE)
                SCREEN_SIZE = GRID_SIZE * CELL_SIZE
                screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), pygame.RESIZABLE)

        # Update the screen
        if play_mode:
            if play_index < len(grid.path) and pygame.time.get_ticks() - play_timer > play_interval:
                play_timer = pygame.time.get_ticks()
                play_index += 1
            show_lines = False
            grid. draw(screen, show_lines, play_index - 1)
            clock.tick(10)
        else:
            # Update the screen
            # grid.update_bullets()
            grid.draw(screen, show_lines)
            if grid.path:
                grid.draw_highlight(screen, *grid.path[-1])
            play_button.draw(screen)
            clock.tick(60)

        #grid.update_bullets()
        pygame.display.flip()
        #clock.tick(60)


if __name__ == "__main__":
    main()
