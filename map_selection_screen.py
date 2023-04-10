import constants
from button import Button


class MapSelectionScreen:
    def __init__(self):
        self.maps = ["Map A", "Map B", "Map C"]
        self.buttons = []

        button_width = 100
        button_height = 40
        button_gap = 20
        total_button_height = len(self.maps) * button_height + (len(self.maps) - 1) * button_gap

        for i, map_name in enumerate(self.maps):
            button_x = (constants.SCREEN_SIZE - button_width) // 2  # Calculate the center x position
            button_y = ((constants.SCREEN_SIZE - total_button_height) // 2) + (i * (button_height + button_gap))  # Calculate the center y position
            button = Button(button_x, button_y, button_width, button_height, map_name, (0, 128, 0), 30)
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

