import pygame
from src.default_sprite import DefaultSprtite


class Ball(DefaultSprtite):
    def __init__(self, parent, color):
        DefaultSprtite.__init__(self, parent, color, (10, 10))
        self.rect = pygame.draw.circle(self.image, self.color, (5, 5), 5)
        self.rect.x = (self.parent.size[0]/2) - (self.rect.width/2)
        self.rect.y = self.parent.size[1] - \
            self.rect.height-self.parent.player.rect.height
        self.update_mask()

    def update(self):
        pass
