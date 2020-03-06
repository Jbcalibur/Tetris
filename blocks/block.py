import pygame
from enum import Enum
from color import Color


class BlockShape(Enum):
    L = (((0, 50), (100, 50), (100, 0), (150, 0), (150, 100), (0, 100)),
         ((0, 75), (100, 25), (150, 25), (150, 75)),
         ((25, 50), (75, 50), (125, 0), (125, 100), (25, 100), (75, 100)),
         (151, 101))
    J = (((0, 0), (150, 0), (150, 100), (100, 100), (100, 50), (0, 50)),
         ((0, 25), (150, 25), (150, 75), (100, 75)),
         ((25, 0), (75, 0), (125, 0), (125, 100), (75, 50), (25, 50)),
         (151, 101))
    O = (((0, 0), (100, 0), (100, 100), (0, 100)),
         ((0, 25), (0, 75), (100, 75), (100, 25)),
         ((25, 0), (75, 0), (75, 100), (25, 100)),
         (101, 101))
    I = (((0, 0), (50, 0), (50, 150), (0, 150)),
         ((0, 25), (0, 75), (0, 125), (50, 125), (50, 75), (50, 25)),
         ((25, 0), (25, 150)),
         (51, 151))
    Z = (((0, 0), (100, 0), (100, 50), (150, 50), (150, 100), (50, 100), (50, 50), (0, 50)),
         ((0, 0),),
         ((0, 0),),
         (151, 101))
    S = (((150, 0), (150, 50), (100, 50), (100, 100), (0, 100), (0, 50), (50, 50), (50, 0)),
         ((50, 25), (150, 25), (0, 75), (100, 75)),
         ((75, 0), (125, 0), (25, 100), (75, 100), (25, 50), (125, 50)),
         (151, 101))
    T = (((0, 0), (150, 0), (150, 50), (100, 50), (100, 100), (50, 100), (50, 50), (0, 50)),
         ((150, 25), (100, 75), (50, 75), (0, 25)),
         ((25, 0), (75, 0), (125, 0), (25, 50), (75, 100), (125, 50),),
         (151, 101))


class Block(pygame.sprite.Sprite):
    def __init__(self, parent, color, shape, position):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.image = pygame.Surface(
            shape.value[-1], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.draw.polygon(self.image, color, shape.value[0])
        for dot in shape.value[1]:
            self.image.set_at(dot, Color.RED.value)
        for dot in shape.value[2]:
            self.image.set_at(dot, Color.BLUE.value)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.move = 0
        self.move_speed = 5

    def update(self):
        side_hit_list = pygame.sprite.spritecollide(
            self, self.parent.block_list, False)[1:]
        floor_hit_list = pygame.sprite.spritecollide(
            self, self.parent.block_list, False)[1:]
        if self.rect.bottom <= self.parent.size[1] and len(floor_hit_list) == 0:
            # self.rect.y += self.move_speed
            pass
        if (self.rect.left + self.move >= 0) and (self.rect.right + self.move <= self.parent.size[0]+self.move_speed) and len(side_hit_list) == 0:
            self.rect.x += self.move

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

    def start_move(self, direction):
        if direction == "left":
            self.move = -self.move_speed
        else:
            self.move = self.move_speed

    def stop_move(self):
        self.move = 0
