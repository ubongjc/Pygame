import pygame

import constants
from constants import *
from button import Button


class GameModeSelectionScreen:
    def __init__(self):
        self.game_modes = ["Single Player", "Two Players"]
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        button_width = 200
        button_height = 50
        button_y_spacing = 20
        start_y = (SCREEN_SIZE - (
                    button_height * len(self.game_modes) + button_y_spacing * (len(self.game_modes) - 1))) // 2

        for index, mode in enumerate(self.game_modes):
            button_x = (SCREEN_SIZE - button_width) // 2
            button_y = start_y + index * (button_height + button_y_spacing)
            button = Button(button_x, button_y, button_width, button_height, mode, (0, 128, 0), 30)
            self.buttons.append(button)

    def draw(self, surface):
        surface.fill(constants.WHITE)
        for button in self.buttons:
            button.draw(surface)

    def check_click(self, x, y):
        for button in self.buttons:
            if button.is_clicked(x, y):
                return True, self.game_modes[self.buttons.index(button)]
        return False, None
