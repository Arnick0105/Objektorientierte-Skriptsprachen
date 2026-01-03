import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CELL_SIZE // 2, CELL_SIZE // 2)

    def move(self, dx, dy, walls):
        # X-Achse
        self.rect.x += dx * PLAYER_SPEED
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                if dx < 0:
                    self.rect.left = wall.right

        # Y-Achse
        self.rect.y += dy * PLAYER_SPEED
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                if dy < 0:
                    self.rect.top = wall.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)
