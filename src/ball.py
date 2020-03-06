from src.default_sprite import DefaultSprtite
import pygame
from random import randint


class Ball(DefaultSprtite):
    def __init__(self, parent, color):
        DefaultSprtite.__init__(self, parent, color, (10, 10))
        self.rect = pygame.draw.circle(self.image, self.color, (5, 5), 5)
        self.set_pos()
        self.velocity = [0, 0]
        self.update_mask()

    def update(self):
        if self.rect.right >= self.parent.size[0]:
            self.velocity[0] = -self.velocity[0]
        if self.rect.left <= 0:
            self.velocity[0] = -self.velocity[0]
        if self.rect.bottom > self.parent.size[1]:
            self.parent.draw_game_over()
            self.velocity = [0, 0]
            self.parent.cursor.execute("""INSERT INTO scores(joueur, score) VALUES(?, ?)""", ("Coco", self.parent.score))
            self.parent.conn.commit()
        if self.rect.top < 0:
            self.velocity[1] = -self.velocity[1]

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def set_pos(self):
        self.rect.centerx, self.rect.centery = self.parent.player.rect.midtop
        self.rect.centery -= (self.rect.height/2)+1

    def move(self, pos):
        self.rect.centerx, self.rect.centery = pos

    def bounce(self, touched_rect):
        if abs(touched_rect.bottom - self.rect.top) <= 5:
            # collide bottom
            self.velocity[1] = -self.velocity[1]
        if abs(touched_rect.top - self.rect.bottom) <= 5:
            # collide top
            self.velocity[1] = -self.velocity[1]
        if abs(touched_rect.left - self.rect.right) <= 5:
            # collide left
            self.velocity[0] = -self.velocity[0]
        if abs(touched_rect.right - self.rect.left) <= 5:
            # collide right
            self.velocity[0] = -self.velocity[0]

    def start(self):
        x = randint(4, 8)
        if x == 0:
            x += 1
        y = randint(-randint(4, 8), randint(4, 8))
        if y == 0:
            y += 1
        self.velocity = [x, y]
