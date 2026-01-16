import pygame
from settings import *

class Gold:
    def __init__(self, x, y):
        self.radius = 8
        self.rect = pygame.Rect(
            x - self.radius,
            y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 215, 0),
            self.rect.center,
            self.radius
        )


