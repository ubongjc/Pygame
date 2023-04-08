import random
import pygame
import sys

from computer_player import ComputerPlayer
from grid import Grid
from constants import *
from map_selection_screen import MapSelectionScreen
from button import Button

# Initialize Pygame
pygame.init()


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

    # Add a new state for the map selection screen
    show_map_selection = True
    map_selection_screen = MapSelectionScreen()
    selected_map = None

    SHOOT_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(SHOOT_EVENT, random.randint(1000, 3000))

    computer_player = ComputerPlayer(grid)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == BULLET_UPDATE_EVENT:
                grid.update_bullets(computer_player.path, play_index-1)
                grid.update_bullets_computer(grid.path, play_index-1)

            # Input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse coordinates
                x, y = pygame.mouse.get_pos()

                # Check if the play button is clicked
                if play_button.is_clicked(x, y):
                    computer_player.path.pop()

                    user_grid_len = len(grid.path)
                    computer_grid_len = len(computer_player.path)

                    if user_grid_len > computer_grid_len:
                        diff_len = user_grid_len - computer_grid_len
                        for i in range(diff_len):
                            computer_player.choose_random_move()

                    print(f"Computer's selected path: {computer_player.path}\n len: {len(computer_player.path)}")  # Print the computer's selected path
                    print(f"user's selected path: {grid.path}\n len: {len(grid.path)}")
                    show_lines = False
                    grid.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    play_mode = True
                    play_index = 0
                    play_timer = pygame.time.get_ticks()

                if not play_mode:
                    # Get cell coordinates
                    cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE

                    # Toggle cell color

                    if len(grid.path) < MAX_MOVES and \
                            grid.is_valid_move(cell_x, cell_y) and \
                            grid.grid[cell_y][cell_x] == 0:
                        grid.grid[cell_y][cell_x] = 1
                        grid.path.append((cell_x, cell_y))
                        grid.fired_bullets.append(False)

                        computer_player.choose_random_move()
                        if computer_player.rollback_to_validity_if_necessary():
                            user_grid_len = len(grid.path)
                            computer_grid_len = len(computer_player.path)
                            if user_grid_len > computer_grid_len:
                                diff_len = user_grid_len - computer_grid_len
                                for i in range(diff_len):
                                    computer_player.choose_random_move()

                    elif grid.path and (cell_x, cell_y) == grid.path[-1]:
                        grid.grid[cell_y][cell_x] = 0
                        grid.path.pop()
                        if len(computer_player.path) > 0:
                            computer_player.path.pop()
                            computer_player.fired_bullets.pop()
                        grid.fired_bullets.pop()

                if show_map_selection:
                    selected_map = map_selection_screen.check_click(x, y)
                    if selected_map:
                        show_map_selection = False
                        print("Selected map:", selected_map)

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
                            grid.fired_bullets[play_index - 1] is False:
                        grid.shoot_bullet(direction, grid.path[play_index - 1], play_index)
                    elif not play_mode:
                        grid.shoot_bullet(direction)

            if play_mode and \
                    play_index < len(computer_player.path) and \
                    computer_player.fired_bullets.count(True) < MAX_BULLETS:
                if event.type == SHOOT_EVENT:
                    # Choose a random position for the computer shooter
                    shooter_x = computer_player.path[play_index-1][0]
                    shooter_y = computer_player.path[play_index-1][1]

                    # Get the direction towards the user
                    direction = grid.get_direction_towards_user(shooter_x, shooter_y)

                    # Shoot the bullet
                    grid.shoot_bullet_computer(direction, start_pos=(shooter_x, shooter_y), computer_player=computer_player)
                    # computer_player.fired_bullets[play_index-1] = True

                    # Reschedule the event with a random interval between 1 and 3 seconds
                    pygame.time.set_timer(SHOOT_EVENT, random.randint(1000, 3000))

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
        if show_map_selection:
            map_selection_screen.draw(screen)
        elif play_mode:
            if play_index < len(grid.path) and pygame.time.get_ticks() - play_timer > play_interval:
                play_timer = pygame.time.get_ticks()
                play_index += 1

            show_lines = False
            grid.draw(screen, show_lines, play_index - 1, computer_player.path)

            clock.tick(10)
        else:
            # Update the screen
            # grid.update_bullets()
            grid.draw(screen, show_lines)
            if grid.path and len(grid.path) < MAX_MOVES:
                grid.draw_highlight(screen, *grid.path[-1])
            else:
                play_button.draw(screen)
            clock.tick(60)

        pygame.display.flip()


if __name__ == "__main__":
    main()
