from src.default_sprite import DefaultSprtite
import pygame


class Platform(DefaultSprtite):
    def __init__(self, parent, color):
        DefaultSprtite.__init__(self, parent, color, (100, 10))
        self.rect = pygame.draw.rect(
            self.image, self.color, (0, 0, *self.size))
        self.rect.x = (self.parent.size[0]/2) - (self.rect.width/2)
        self.rect.y = self.parent.size[1]-self.rect.height
        self.move = 0
        self.move_speed = 10
        self.update_mask()

    def update(self):
        brick_hit_list = pygame.sprite.spritecollide(
            self, self.parent.brick_list, False)[1:]
        ball_hit_list = pygame.sprite.spritecollide(
            self, self.parent.ball_list, False, collided=pygame.sprite.collide_mask)
        if (self.rect.left + self.move >= 0) and (self.rect.right + self.move <= self.parent.size[0]+self.move_speed) and len(brick_hit_list) == 0:
            self.rect.x += self.move
        for hit in ball_hit_list:
            self.parent.ball.bounce(self.rect)

    def start_move(self, direction):
        if direction == "left":
            self.move = -self.move_speed
        else:
            self.move = self.move_speed

    def stop_move(self):
        self.move = 0
