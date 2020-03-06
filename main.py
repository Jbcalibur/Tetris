import pygame
from pygame import locals as pygame_locals
from src import Platform, Brick, Ball
from functools import partial
from color import Color

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
        self.name = name
        self.size = size
        self.in_progress = False
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

        tmp = Ball(self, Color.RED)
        self.ball_list.add(tmp)
        self.all_sprites_list.add(tmp)

        tmp = Brick(self, Color.BLUE, (0,0))
        self.brick_list.add(tmp)
        self.all_sprites_list.add(tmp)

    def start(self):
        self.in_progress = True

        pygame.display.update()
        while self.in_progress:
            for event in pygame.event.get():
                if event.type in self.event_map:
                    self.event_map[event.type](event)
            self.window.fill(Color.WHITE.value)
            self.all_sprites_list.update()
            self.all_sprites_list.draw(self.window)
            self.clock.tick(30)
            pygame.display.flip()
        pygame.quit()

    def _stop(self, event):
        self.in_progress = False

    def _handle_key_down(self, event):
        key_map = {
            276: partial(self._move_player, "left", True),
            275: partial(self._move_player, "right", True),
        }
        if event.key in key_map:
            key_map[event.key]()
        print("down {}".format(event.key))

    def _handle_key_up(self, event):
        key_map = {
            276: partial(self._move_player, "left", False),
            275: partial(self._move_player, "right", False),
        }
        if event.key in key_map:
            key_map[event.key]()
        print("up {}".format(event.key))
    
    def _move_player(self, direction, state):
        if state:
            self.player.start_move(direction)
        else:
            self.player.stop_move()


if __name__ == "__main__":
    create_application("Tetris", (500, 500)).start()
