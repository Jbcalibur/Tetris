import pygame
from pygame import locals as pygame_locals
from blocks.block import Block, BlockShape
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
        self.current = None
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

    def start(self):
        self.in_progress = True

        self.current = Block(self, Color.SILVER.value, BlockShape.I, (50, 300))
        self.block_list.add(self.current)
        self.all_sprites_list.add(self.current)

        self.current = Block(self, Color.YELLOW.value, BlockShape.L, (0, 0))
        self.current.rotate(180)
        self.block_list.add(self.current)
        self.all_sprites_list.add(self.current)

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
            276: partial(self._move_curent, "left", True),
            273: partial(self._rotate_current, "left"),
            275: partial(self._move_curent, "right", True),
            274: partial(self._rotate_current, "right"),
        }
        if event.key in key_map:
            key_map[event.key]()
        print("down {}".format(event.key))

    def _handle_key_up(self, event):
        key_map = {
            276: partial(self._move_curent, "left", False),
            275: partial(self._move_curent, "right", False),
        }
        if event.key in key_map:
            key_map[event.key]()
        print("up {}".format(event.key))
    
    def _move_curent(self, direction, state):
        if state:
            self.current.start_move(direction)
        else:
            self.current.stop_move()

    def _rotate_current(self, direction):
        if direction == "left":
            self.current.rotate(-90)
        else:
            self.current.rotate(90)


if __name__ == "__main__":
    create_application("Tetris", (500, 500)).start()
