import pygame
import constants
from constants import *
from button import Button


class IntroScreen:
    def __init__(self):
        self.button = None
        self.create_buttons()
        self.intro_image = pygame.image.load("images/intro.png")

    def create_buttons(self):
        button_width = 200
        button_height = 50
        button_y_spacing = 20
        start_y = 400
        button_x = (SCREEN_SIZE - button_width) // 2
        button_y = 400
        self.button = Button(button_x, button_y, button_width, button_height, "START", (0, 128, 0), 30)

    def draw(self, surface):
        surface.blit(self.intro_image, (0, 0))
        self.button.draw(surface)

    def check_click(self, x, y):
        if self.button.is_clicked(x, y):
            return True
        return False
