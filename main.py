import random
import pygame
import sys

import constants
from computer_player import ComputerPlayer
from grid import Grid
# from constants import *
from map_selection_screen import MapSelectionScreen
from button import Button

# Initialize Pygame
pygame.init()


# Main function
def main():
    # Get the user's screen size
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Calculate the appropriate cell size
    constants.CELL_SIZE = min(screen_width, screen_height) // constants.GRID_SIZE
    constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE

    screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Grid Game")
    clock = pygame.time.Clock()
    bullet_update_event = pygame.USEREVENT + 1
    pygame.time.set_timer(bullet_update_event, 500)  # Set the interval to 500ms

    grid = Grid(constants.GRID_SIZE)
    grid.bullet_start_indices = []
    show_lines = True

    # play button
    button_width = 100
    button_height = 40
    button_x = (constants.SCREEN_SIZE - button_width) // 2  # Calculate the center x position
    button_y = (constants.SCREEN_SIZE - button_height) // 2  # Calculate the center y position
    play_button = Button(button_x, button_y, button_width, button_height, "Play", (0, 128, 0), 30)

    play_mode = False
    play_index = 0
    play_timer = 0
    play_interval = 1000  # Time interval in milliseconds between path cells

    # Add a new state for the map selection screen
    show_map_selection = True
    map_selection_screen = MapSelectionScreen()

    shoot_event = pygame.USEREVENT + 2
    pygame.time.set_timer(shoot_event, random.randint(1000, 3000))

    computer_player = ComputerPlayer(grid)
    screen_resized = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == bullet_update_event:
                grid.update_bullets(computer_player.path, play_index - 1)
                grid.update_bullets_computer(grid.path, play_index - 1)

            # Input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse coordinates
                x, y = pygame.mouse.get_pos()

                # Check if the play button is clicked
                if play_button.is_clicked(x, y) and \
                        len(grid.path) >= constants.MAX_MOVES and \
                        not play_mode:
                    # computer_player.path.pop()

                    # user_grid_len = len(grid.path)
                    # computer_grid_len = len(computer_player.path)
                    #
                    # if user_grid_len > computer_grid_len:
                    #     diff_len = user_grid_len - computer_grid_len
                    #     for i in range(diff_len):
                    #         computer_player.choose_random_move()

                    print(f"Computer's selected path: {computer_player.path}\n len: {len(computer_player.path)}")
                    print(f"user's selected path: {grid.path}\n len: {len(grid.path)}")
                    show_lines = False
                    grid.grid = [[0 for _ in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)]
                    play_mode = True
                    play_index = 0
                    play_timer = pygame.time.get_ticks()

                if not play_mode:
                    # Get cell coordinates
                    cell_x, cell_y = x // constants.CELL_SIZE, y // constants.CELL_SIZE

                    # Toggle cell color

                    if len(grid.path) < constants.MAX_MOVES and \
                            grid.is_valid_move(cell_x, cell_y) and \
                            grid.grid[cell_y][cell_x] == 0:
                        grid.grid[cell_y][cell_x] = 1
                        grid.path.append((cell_x, cell_y))
                        grid.fired_bullets.append(False)

                        # computer_player.choose_random_move()
                        # if computer_player.rollback_to_validity_if_necessary():
                        #     user_grid_len = len(grid.path)
                        #     computer_grid_len = len(computer_player.path)
                        #     if user_grid_len > computer_grid_len:
                        #         diff_len = user_grid_len - computer_grid_len
                        #         for i in range(diff_len):
                        #             computer_player.choose_random_move()

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
                    computer_player.fired_bullets.count(True) < constants.MAX_BULLETS:
                if event.type == shoot_event:
                    # Choose a random position for the computer shooter
                    shooter_x = computer_player.path[play_index - 1][0]
                    shooter_y = computer_player.path[play_index - 1][1]

                    # Get the direction towards the user
                    direction = grid.get_direction_towards_user(shooter_x, shooter_y)

                    # Shoot the bullet
                    grid.shoot_bullet_computer(direction, start_pos=(shooter_x, shooter_y),
                                               computer_player=computer_player)
                    # computer_player.fired_bullets[play_index-1] = True

                    # Reschedule the event with a random interval between 1 and 3 seconds
                    pygame.time.set_timer(shoot_event, random.randint(1000, 3000))

            # Toggle grid lines
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_lines = not show_lines

            # Resize the screen
            if event.type == pygame.VIDEORESIZE:
                #screen_resized = True
                width, height = event.w, event.h
                constants.CELL_SIZE = min(width // constants.GRID_SIZE, height // constants.GRID_SIZE)
                constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
                screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)

        # if screen_resized:
        #     screen_resized = False
        #     screen.fill(constants.WHITE)
        #     grid.draw(screen)
        #     pygame.display.flip()

        # reset game
        if not grid.winner and play_index == len(grid.path) and \
                play_index > 0:
            if constants.GRID_SIZE > 5:
                constants.GRID_SIZE -= 1
                constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
                constants.MAX_MOVES = constants.GRID_SIZE * 2
                constants.MAX_BULLETS = constants.MAX_MOVES // 2
                screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)
                grid = Grid(constants.GRID_SIZE)
                computer_player = ComputerPlayer(grid)
                show_lines = True
                play_mode = False
                play_index = 0
                play_timer = 0

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
            grid.draw(screen, show_lines)
            if grid.path and len(grid.path) < constants.MAX_MOVES:
                grid.draw_highlight(screen)
            elif grid.path and len(grid.path) >= constants.MAX_MOVES:
                play_button.draw(screen)
            clock.tick(60)

        pygame.display.flip()


if __name__ == "__main__":
    main()
