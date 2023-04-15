import random
import pygame
import sys
import constants

from grid import Grid
from map_selection_screen import MapSelectionScreen
from button import Button
from players.user_player import UserPlayer
from players.computer_player import ComputerPlayer
from game_mode_selection_screen import GameModeSelectionScreen


# Initialize Pygame
pygame.init()


def draw_play_button():
    # play button
    button_width = 100
    button_height = 40
    button_x = (constants.SCREEN_SIZE - button_width) // 2  # Calculate the center x position
    button_y = (constants.SCREEN_SIZE - button_height) // 2  # Calculate the center y position
    return Button(button_x, button_y, button_width, button_height, "Play", (0, 128, 0), 30)


def handle_instruction_button_click(show_instructions, instruction_button, x, y):
    if show_instructions and instruction_button.is_clicked(x, y):
        return False, True
    return show_instructions, False


def handle_play_button_click(play_button, x, y, player, computer_player, play_mode, grid):
    if play_button.is_clicked(x, y) and len(player.path) >= constants.MAX_MOVES and not play_mode:
        print(f"Computer's selected path: {computer_player.path}\n len: {len(computer_player.path)}")
        print(f"user's selected path: {player.path}\n len: {len(player.path)}")
        grid.grid = [[0 for _ in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)]
        return False, True, 0, pygame.time.get_ticks()
    return True, play_mode, -1, -1


def handle_path_editing(x, y, play_mode, player, computer_player, grid):
    if not play_mode:
        cell_x, cell_y = x // constants.CELL_SIZE, y // constants.CELL_SIZE
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


def handle_map_selection(x, y, show_map_selection, map_selection_screen):
    if show_map_selection:
        selected_map = map_selection_screen.check_click(x, y)
        if selected_map:
            show_map_selection = False
            print("Selected map:", selected_map)
    return False


def handle_game_mode_options_selection(x, y, show_game_mode_options, game_mode_selection_screen):
    if show_game_mode_options:
        selected_mode = game_mode_selection_screen.check_click(x, y)
        if selected_mode:
            show_game_mode_options = False
            print("Selected mode:", selected_mode)
    return show_game_mode_options, True


def handle_bullet_shoot(event, play_mode, play_index, player):
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
            if play_mode and play_index > 0 and player.fired_bullets[play_index - 1] is False:
                player.shoot_bullet(direction, current_path_index=play_index)


def handle_computer_shoot(event, play_mode, play_index, computer_player, player, shoot_event):
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
            pygame.time.set_timer(shoot_event, random.randint(1000, 3000))


def toggle_grid_lines(event, show_lines):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            show_lines = not show_lines
    return show_lines


def resize_screen(event, screen):
    if event.type == pygame.VIDEORESIZE:
        constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
        screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)
    return screen


def update_grid_and_screen(screen, player, computer_player, grid, player_image, computer_player_image, show_lines,
                           play_mode, play_index, play_timer):
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
    return screen, player, computer_player, grid, show_lines, play_mode, play_index, play_timer


def reset_game(screen, player, computer_player, grid, player_image, computer_player_image, show_lines, play_mode, play_index, play_timer):
    if not grid.winner and play_index == len(player.path) and play_index > 0:
        round_number = 11 - (constants.MAX_BULLETS - 1)
        texts = [
            f"Draw - Round {round_number}",
            f"{constants.MAX_MOVES - 2} moves"
        ]
        display_centered_texts(screen, texts, font_size=50, color=constants.BLACK)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds (2000 ms)
        screen, player, computer_player, grid, show_lines, play_mode, play_index, play_timer = \
            update_grid_and_screen(screen, player, computer_player, grid, player_image, computer_player_image,
                                   show_lines, play_mode, play_index, play_timer)
    return screen, player, computer_player, grid, show_lines, play_mode, play_index, play_timer


def update_play_index_and_draw_grid(screen, grid, play_index, play_timer, play_interval, show_lines, clock, player):
    if play_index < len(player.path) and pygame.time.get_ticks() - play_timer > play_interval:
        play_timer = pygame.time.get_ticks()
        play_index += 1
    show_lines = False
    grid.draw(screen, show_lines, play_index - 1)
    clock.tick(10)
    return play_index, play_timer, show_lines


def draw_game_elements(screen, grid, player, play_button, show_lines, clock):
    grid.draw(screen, show_lines)
    if player.path and len(player.path) < constants.MAX_MOVES:
        grid.draw_highlight(screen)
    elif player.path and len(player.path) >= constants.MAX_MOVES:
        play_button = draw_play_button()
        play_button.draw(screen)
    clock.tick(60)


def display_scaled_background_and_button(screen, background_image, instructions):
    scaled_background = pygame.transform.scale(background_image, (constants.SCREEN_SIZE, constants.SCREEN_SIZE))
    screen.blit(scaled_background, (0, 0))
    last_line_y = display_centered_texts(screen, instructions, font_size=50, color=constants.BLACK)
    instruction_button_y = last_line_y + 20  # Add some space (20 pixels) between the last line and the button
    instruction_button = Button((constants.SCREEN_SIZE - 150) // 2, instruction_button_y, 150, 40, "Continue",
                                (0, 128, 0), 30)
    instruction_button.draw(screen)
    return instruction_button


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


def handle_quit_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


# Main function
def main():
    # Calculate the appropriate cell size
    constants.SCREEN_SIZE = constants.GRID_SIZE * constants.CELL_SIZE
    screen = pygame.display.set_mode((constants.SCREEN_SIZE, constants.SCREEN_SIZE), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Grid Game")
    clock = pygame.time.Clock()
    bullet_update_event = pygame.USEREVENT + 1
    pygame.time.set_timer(bullet_update_event, 500)  # Set the interval to 500ms
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
    game_mode_selection_screen = GameModeSelectionScreen()  # Add this line
    shoot_event = pygame.USEREVENT + 2
    pygame.time.set_timer(shoot_event, random.randint(1000, 3000))
    show_instructions = True
    instructions = ["Instruction 1", "Instruction 2", "Instruction 3"]
    instruction_button = None
    show_game_mode_options = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                handle_quit_event(event)

            if event.type == bullet_update_event:
                grid.update_bullets(play_index)

            # Input handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                show_instructions, show_game_mode_options = \
                    handle_instruction_button_click(show_instructions, instruction_button, x, y)
                show_lines, play_mode, play_index, play_timer = \
                    handle_play_button_click(play_button, x, y, player, computer_player, play_mode, grid)
                handle_path_editing(x, y, play_mode, player, computer_player, grid)
                show_game_mode_options, show_map_selection = \
                    handle_game_mode_options_selection(x, y, show_game_mode_options, game_mode_selection_screen)
                show_map_selection = handle_map_selection(x, y, show_map_selection, map_selection_screen)
                print(show_map_selection)

            handle_bullet_shoot(event, play_mode, play_index, player)
            handle_computer_shoot(event, play_mode, play_index, computer_player, player, shoot_event)
            show_lines = toggle_grid_lines(event, show_lines)
            screen = resize_screen(event, screen)

        # reset game
        screen, player, computer_player, grid, show_lines, play_mode, play_index, play_timer = \
            reset_game(screen, player, computer_player, grid, player_image, computer_player_image, show_lines,
                       play_mode, play_index, play_timer)

        # Update the screen
        if show_instructions:
            instruction_button = display_scaled_background_and_button(screen, background_image, instructions)
        elif show_game_mode_options:
            game_mode_selection_screen.draw(screen)
        elif show_map_selection:
            print(f"wone {show_map_selection}")
            map_selection_screen.draw(screen)
        elif play_mode:
            play_index, play_timer, show_lines = \
                update_play_index_and_draw_grid(screen, grid, play_index, play_timer, play_interval, show_lines, clock,
                                                player)
        else:
            draw_game_elements(screen, grid, player, play_button, show_lines, clock)

        pygame.display.flip()


if __name__ == "__main__":
    main()
