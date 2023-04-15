import constants
from button import Button


class GameModeSelectionScreen:
    def __init__(self):
        self.modes = ["Single Player", "Two Players"]
        self.buttons = []

        button_width = 200
        button_height = 40
        button_gap = 20
        total_button_height = len(self.modes) * button_height + (len(self.modes) - 1) * button_gap

        for i, mode_name in enumerate(self.modes):
            button_x = (constants.SCREEN_SIZE - button_width) // 2  # Calculate the center x position
            button_y = ((constants.SCREEN_SIZE - total_button_height) // 2) + (i * (button_height + button_gap))  # Calculate the center y position
            button = Button(button_x, button_y, button_width, button_height, mode_name, (0, 128, 0), 30)
            self.buttons.append(button)

    def draw(self, surface):
        surface.fill(constants.WHITE)
        for button in self.buttons:
            button.draw(surface)

    def check_click(self, x, y):
        for button in self.buttons:
            if button.is_clicked(x, y):
                return button.text
        return None
