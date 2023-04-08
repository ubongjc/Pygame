from constants import *
from button import Button

class MapSelectionScreen:
    def __init__(self):
        self.maps = ["Map A", "Map B", "Map C"]
        self.buttons = []
        button_width = int(SCREEN_SIZE * 0.2)
        button_height = int(SCREEN_SIZE * 0.1)
        button_spacing = int(SCREEN_SIZE * 0.1)
        button_y = SCREEN_SIZE // 2

        for i, map_name in enumerate(self.maps):
            button = Button(SCREEN_SIZE // 2 - 50, 150 * (i + 1), 100, 40, map_name, (0, 128, 0), 30)
            # button = Button((SCREEN_SIZE - button_width) // 2 - button_spacing - button_width, button_y, button_width, button_height, map_name, (0, 128, 0), 30),

            self.buttons.append(button)

    def draw(self, surface):
        surface.fill(WHITE)
        for button in self.buttons:
            button.draw(surface)

    def check_click(self, x, y):
        for button in self.buttons:
            if button.is_clicked(x, y):
                return button.text
        return None

