from pygame import locals as pygame_locals
from src import Platform, Brick, Ball
from functools import partial
from color import Color
import pygame

__inst__ = None


def create_application(name, size):
    global __inst__
    if __inst__ is None:
        __inst__ = Application(name, size)
        return __inst__
    else:
        raise Exception("Application already exist")


def get_application():
    global __inst__
    if __inst__ is not None:
        return __inst__
    else:
        raise Exception("Application doesn't exist")


class Application():
    def __init__(self, name, size):
        pygame.init()
        self.score = 0
        self.name = name
        self.size = size
        self.in_progress = False
        self.started = False
        pygame.display.set_caption(self.name)
        self.window = pygame.display.set_mode(self.size)
        self.window.fill(Color.WHITE.value)
        self.clock = pygame.time.Clock()
        self.event_map = {
            pygame_locals.QUIT: self._stop,
            pygame_locals.KEYDOWN: self._handle_key_down,
            pygame_locals.KEYUP: self._handle_key_up,
        }
        self.ball_list = pygame.sprite.Group()
        self.brick_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        self.player = Platform(self, Color.SILVER)
        self.all_sprites_list.add(self.player)

        self.ball = Ball(self, Color.RED)
        self.ball_list.add(self.ball)
        self.all_sprites_list.add(self.ball)

    def init_brick_list(self):
        brick_size = (50, 25)
        y = 0
        for _ in range(0, 5):
            x = 0
            for target_list in range(0, int(self.size[0]/brick_size[0])):
                tmp = Brick(self, (x, y), brick_size)
                self.brick_list.add(tmp)
                self.all_sprites_list.add(tmp)
                x += brick_size[0]
            y += brick_size[1]

    def start(self):
        self.in_progress = True

        pygame.display.update()
        while self.in_progress:
            if len(self.brick_list.sprites()) == 0:
                self.init_brick_list()
            for event in pygame.event.get():
                if event.type in self.event_map:
                    self.event_map[event.type](event)
            self.window.fill(Color.WHITE.value)
            self.all_sprites_list.update()
            self.all_sprites_list.draw(self.window)
            print(self.score)
            self.clock.tick(30)
            pygame.display.flip()

    def _stop(self, event):
        pygame.quit()

    def _handle_key_down(self, event):
        key_map = {
            276: partial(self._move_player, "left", True),
            275: partial(self._move_player, "right", True),
            32: self._start
        }
        if event.key in key_map:
            key_map[event.key]()

    def _handle_key_up(self, event):
        key_map = {
            276: partial(self._move_player, "left", False),
            275: partial(self._move_player, "right", False),
        }
        if event.key in key_map:
            key_map[event.key]()

    def _move_player(self, direction, state):
        if state:
            self.player.start_move(direction)
        else:
            self.player.stop_move()
    
    def _start(self):
        if not self.started:
            self.started = True
            self.ball.start()


if __name__ == "__main__":
    create_application("BrickBreaker", (500, 250)).start()
