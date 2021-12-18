import os
import time

try:
    # Import pygame if it is installed, fail safe
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
except ImportError:
    pygame = None


__all__ = [
    "Color", "PyGameVisualise"
]


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (64, 64, 64)
    ORANGE = (252, 186, 3)
    RED = (252, 0, 0)
    BROWN = (150, 117, 60)
    GREEN = (9, 181, 66)


class PyGameVisualise:
    """ Wrapper for pygame for visualisations """
    # Class singleton to prevent a second window from being created
    _pygame_init = False

    def __init__(self, x, y, display_scale=10, color=Color.GREY):
        self._x = x
        self._y = y
        self._display_scale = display_scale
        self._quit = False
        self._init = False
        self.screen = None
        if pygame is not None and not self.__class__._pygame_init:
            self._init = True
            self.__class__._pygame_init = True
            pygame.init()
            self.screen = pygame.display.set_mode((self.scale(x + 1), self.scale(y + 1)))
            self.fill(color)

    def run_event_loop(self):
        """ Run pygame event loop """
        if self._init and not self._quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._quit = True
                    break
                else:
                    self._event_loop_callback(event)

    def check_quit(self, timeout=None):
        """" Check if pygame window has quit. If timeout is supplied, wait up to timeout seconds """
        if self._init:
            _time = time.time()
            while not self._quit:
                self.run_event_loop()
                if timeout is None or (time.time() - _time) > timeout:
                    break
            return self._quit
        else:
            return True

    def fill(self, color):
        """ Fill screen with color """
        if self._init and not self._quit:
            self.screen.fill(color)

    def draw_block(self, x, y, color, gap=0):
        """ Draw a block at (scaled) x and y. Block will be 1 scaled unit minus gap, to allow gaps between blocks """
        if self._init and not self._quit:
            coords = [self.scale(x), self.scale(y), self._display_scale - gap, self._display_scale - gap]
            pygame.draw.rect(self.screen, color, coords)

    def draw(self, framerate=None):
        """ Update screen """
        if self._init and not self._quit:
            self.run_event_loop()
            pygame.display.update()
            pygame.time.Clock().tick(framerate or 0)

    def scale(self, v):
        """ Scale blocks to screen size """
        return v * self._display_scale

    def _event_loop_callback(self, event):
        """ Subclasses may handle more events """
        pass
