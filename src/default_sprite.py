import pygame


class DefaultSprtite(pygame.sprite.Sprite):
    def __init__(self, parent, color, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.color = color.value
        self.parent = parent
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
    
    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
