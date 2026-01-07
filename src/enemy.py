import pygame
import random
from settings import *

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, CELL_SIZE // 2, CELL_SIZE // 2)
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

    def update(self, walls):
        if random.randint(0, 100) < 2:
            self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

        dx, dy = self.direction

        self.rect.x += dx * ENEMY_SPEED
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.x -= dx * ENEMY_SPEED
                self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                return

        self.rect.y += dy * ENEMY_SPEED
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect.y -= dy * ENEMY_SPEED
                self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                return

    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.rect.x, self.rect.y + UI_HEIGHT, self.rect.width, self.rect.height))
