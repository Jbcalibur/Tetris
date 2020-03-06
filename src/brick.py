from src.default_sprite import DefaultSprtite
from color import Color
import pygame
from random import randint


class Brick(DefaultSprtite):
    def __init__(self, parent, position, size):
        self.state_color = {
            5: Color.GREEN,
            4: Color.CYAN,
            3: Color.BLUE,
            2: Color.PURPLE,
            1: Color.RED,
            0: Color.YELLOW,
        }
        self.state = randint(0,5)
        DefaultSprtite.__init__(self, parent, self.state_color[self.state], (size, size))
        self.rect = self.draw()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.update_mask()

    def draw(self):
        self.color = self.state_color[self.state].value
        rect = pygame.draw.rect(
            self.image, self.color, (0, 0, *self.size))
        pygame.draw.rect(self.image, Color.BLACK.value, (0, 0, self.size[0]-1, self.size[1]-1), 2)
        return rect
        

    def update(self):
        ball_hit_list = pygame.sprite.spritecollide(
            self, self.parent.ball_list, False, collided=pygame.sprite.collide_mask)
        for hit in ball_hit_list:
            if self.state > 0:
                self.state -=1
                self.draw()
                self.parent.ball.bounce(self.rect)
            else:
                self.parent.ball.bounce(self.rect)
                self.kill()
        
