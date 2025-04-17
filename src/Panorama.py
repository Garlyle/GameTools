import numpy as np
import pygame

class Panorama(pygame.Surface):
    """Scrolling background image"""

    def __init__(self, filename, size, speed=(0,0)):
        """Creates a continuous image for given size, scrolls with given speed"""
        self.image = pygame.image.load(filename)
        self.resize(size)
        self.speed = speed
        self.position = pygame.Vector2(0,0)

    def update(self, delta):
        """calculates movement over time"""
        self.position.x += self.speed[0] * delta
        self.position.y += self.speed[1] * delta
        self.scroll(int(self.position.x), int(self.position.y), pygame.SCROLL_REPEAT)
        self.position.x -= int(self.position.x)
        self.position.y -= int(self.position.y)

    def resize(self, size):
        """Change the given size for rendering"""
        xcoords = np.arange(0, size[0], step = self.image.width)
        ycoords = np.arange(0, size[1], step = self.image.height)
        super().__init__((self.image.width * len(xcoords), self.image.height * len(ycoords)))
        # combine x and y coords
        allcoords = np.array(np.meshgrid(xcoords,ycoords)).T.reshape(-1,2)
        # pair image with all coords to pass for blits
        imgarray = np.repeat(self.image, len(allcoords))
        renderlist = list(zip(imgarray, allcoords))

        self.blits(renderlist)
