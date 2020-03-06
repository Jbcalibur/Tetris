import pygame
from src.default_sprite import DefaultSprtite


class Brick(DefaultSprtite):
    def __init__(self, parent, color, position):
        DefaultSprtite.__init__(self, parent, color, (25, 25))
        self.rect = pygame.draw.rect(self.image, self.color, (0, 0, *self.size))
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.update_mask()

    def update(self):
        pass