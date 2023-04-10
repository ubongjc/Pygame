import constants
from button import Button

class MapSelectionScreen:
    def __init__(self):
        self.maps = ["Map A", "Map B", "Map C"]
        self.buttons = []
        button_width = int(constants.SCREEN_SIZE * 0.2)
        button_height = int(constants.SCREEN_SIZE * 0.1)
        button_spacing = int(constants.SCREEN_SIZE * 0.1)
        button_y = constants.SCREEN_SIZE // 2

        for i, map_name in enumerate(self.maps):
            button = Button(constants.SCREEN_SIZE // 2 - 50, 150 * (i + 1), 100, 40, map_name, (0, 128, 0), 30)

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

