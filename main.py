import random
import pygame
import sys

import constants
from grid import Grid
from map_selection_screen import MapSelectionScreen
from button import Button
from players.user_player import UserPlayer
from players.computer_player import ComputerPlayer

# Initialize Pygame
pygame.init()


def draw_play_button():
    # play button
    button_width = 100
    button_height = 40
    button_x = (constants.SCREEN_SIZE - button_width) // 2  # Calculate the center x position
    button_y = (constants.SCREEN_SIZE - button_height) // 2  # Calculate the center y position
    return Button(button_x, button_y, button_width, button_height, "Play", (0, 128, 0), 30)


def display_centered_texts(screen, texts, font_size, color, line_spacing=10):
    screen_width, screen_height = screen.get_size()

    # Create a font object
    font = pygame.font.Font(None, font_size)

    # Calculate the total height of all lines of text
    total_text_height = len(texts) * font.get_height() + (len(texts) - 1) * line_spacing

    # Calculate the starting Y position for the first line of text
    start_y = (screen_height - total_text_height) // 2

    pos_y = -1
    text_height = -1

    for i, text in enumerate(texts):
        # Render the text and get its surface
        text_surface = font.render(text, True, color)
        # Calculate the position of the text
        text_width, text_height = text_surface.get_size()
        pos_x = (screen_width - text_width) // 2
        pos_y = start_y + i * (text_height + line_spacing)
        # Blit the text surface onto the screen
        screen.blit(text_surface, (pos_x, pos_y))
    return pos_y + text_height


# Main function
def main():
    # Calculate the appropriate cell size
    constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
    screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Grid Game")
    clock = pygame.time.Clock()
    BULLET_UPDATE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BULLET_UPDATE_EVENT, 500)  # Set the interval to 500ms

    # Load player and computer player images
    player_image = "images/user_2.png"
    computer_player_image = "images/user_2.png"
    background_image = pygame.image.load("images/background.png")

    player = UserPlayer(player_image, -1, -1)
    computer_player = ComputerPlayer(computer_player_image, -1, -1)

    grid = Grid(constants.GRID_SIZE, player, computer_player)
    show_lines = True
    play_button = draw_play_button()

    play_mode = False
    play_index = 0
    play_timer = 0
    play_interval = 1000  # Time interval in milliseconds between path cells

    # Add a new state for the map selection screen
    show_map_selection = False
    map_selection_screen = MapSelectionScreen()

    shoot_event = pygame.USEREVENT + 2
    pygame.time.set_timer(shoot_event, random.randint(1000, 3000))

    show_instructions = True
    instructions = ["Instruction 1", "Instruction 2", "Instruction 3"]
    instruction_button = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == BULLET_UPDATE_EVENT:
                grid.update_bullets(play_index)

            # Input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse coordinates
                x, y = pygame.mouse.get_pos()

                if show_instructions and instruction_button.is_clicked(x, y):
                    show_instructions = False
                    show_map_selection = True
                    print("something")

                # Check if the play button is clicked
                if play_button.is_clicked(x, y) and \
                        len(player.path) >= constants.MAX_MOVES and \
                        not play_mode:

                    print(f"Computer's selected path: {computer_player.path}\n len: {len(computer_player.path)}")
                    print(f"user's selected path: {player.path}\n len: {len(player.path)}")
                    show_lines = False
                    grid.grid = [[0 for _ in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)]
                    play_mode = True
                    play_index = 0
                    play_timer = pygame.time.get_ticks()

                if not play_mode:
                    # Get cell coordinates
                    cell_x, cell_y = x // constants.CELL_SIZE, y // constants.CELL_SIZE

                    # Toggle cell color
                    if len(player.path) < constants.MAX_MOVES and \
                            player.is_valid_move(cell_x, cell_y) and \
                            grid.grid[cell_y][cell_x] == 0:
                        grid.grid[cell_y][cell_x] = 1
                        player.path.append((cell_x, cell_y))
                        player.fired_bullets.append(False)

                    elif player.path and (cell_x, cell_y) == player.path[-1]:
                        grid.grid[cell_y][cell_x] = 0
                        player.path.pop()
                        if len(computer_player.path) > 0:
                            computer_player.path.pop()
                            computer_player.fired_bullets.pop()
                        player.fired_bullets.pop()

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
                            player.fired_bullets[play_index - 1] is False:
                        player.shoot_bullet(direction, current_path_index=play_index)

            if play_mode and \
                    play_index < len(computer_player.path) and \
                    computer_player.fired_bullets.count(True) < constants.MAX_BULLETS:
                if event.type == shoot_event:
                    # Choose a random position for the computer shooter
                    shooter_x = computer_player.path[play_index - 1][0]
                    shooter_y = computer_player.path[play_index - 1][1]

                    # Get the direction towards the user
                    direction = computer_player.get_direction_towards_user(player.path, shooter_x, shooter_y)

                    # Shoot the bullet
                    computer_player.shoot_bullet_computer(direction, current_path_index=play_index)
                    # grid.shoot_bullet_computer(direction, start_pos=(shooter_x, shooter_y),
                    #                            computer_player=computer_player)
                    # computer_player.fired_bullets[play_index-1] = True

                    # Reschedule the event with a random interval between 1 and 3 seconds
                    pygame.time.set_timer(shoot_event, random.randint(1000, 3000))

            # Toggle grid lines
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_lines = not show_lines

            # Resize the screen
            if event.type == pygame.VIDEORESIZE:
                constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
                screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)

        # reset game
        if not grid.winner and play_index == len(player.path) and \
                play_index > 0:
            # Display "Draw - Round 2" text
            round_number = 11 - (constants.MAX_BULLETS - 1)
            texts = [
                f"Draw - Round {round_number}",
                f"{constants.MAX_MOVES - 2} moves"
            ]
            display_centered_texts(screen, texts, font_size=50, color=constants.BLACK)

            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds (2000 ms)

            if constants.GRID_SIZE > 5:
                constants.GRID_SIZE -= 1
                constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
                constants.MAX_MOVES = constants.GRID_SIZE * 2
                constants.MAX_BULLETS = constants.MAX_MOVES // 2
                screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)
                player = UserPlayer(player_image, -1, -1)
                computer_player = ComputerPlayer(computer_player_image, -1, -1)
                grid = Grid(constants.GRID_SIZE, player, computer_player)
                show_lines = True
                play_mode = False
                play_index = 0
                play_timer = 0

        # Update the screen
        if show_instructions:
            scaled_background = pygame.transform.scale(background_image, (constants.SCREEN_SIZE, constants.SCREEN_SIZE))
            screen.blit(scaled_background, (0, 0))
            last_line_y = display_centered_texts(screen, instructions, font_size=50, color=constants.BLACK)
            instruction_button_y = last_line_y + 20  # Add some space (20 pixels) between the last line and the button
            instruction_button = Button((constants.SCREEN_SIZE - 150) // 2, instruction_button_y, 150, 40, "Continue",
                                        (0, 128, 0), 30)
            instruction_button.draw(screen)
        elif show_map_selection:
            map_selection_screen.draw(screen)
        elif play_mode:
            if play_index < len(player.path) and pygame.time.get_ticks() - play_timer > play_interval:
                play_timer = pygame.time.get_ticks()
                play_index += 1

            show_lines = False
            grid.draw(screen, show_lines, play_index - 1)

            clock.tick(10)
        else:
            grid.draw(screen, show_lines)
            if player.path and len(player.path) < constants.MAX_MOVES:
                grid.draw_highlight(screen)
            elif player.path and len(player.path) >= constants.MAX_MOVES:
                play_button = draw_play_button()
                play_button.draw(screen)
            clock.tick(60)

        pygame.display.flip()


if __name__ == "__main__":
    main()
