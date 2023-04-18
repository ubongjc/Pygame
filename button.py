import pygame

import constants
from constants import *


class Button:
    def __init__(self, x, y, width, height, text, color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = constants.BUTTON_COLOR
        self.font_size = font_size
        self.font = pygame.font.Font("fonts/Mister Pixel Regular.otf", 16)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, constants.BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text, text_rect)

    def is_clicked(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

