import pygame
import math
from settings import *

class FireBarEnemy:
    def __init__(self, center_x, center_y, length, speed):
        self.center_x = center_x
        self.center_y = center_y

        self.length = length + 2             # Anzahl Segmente
        self.segment_radius = 10
        self.segment_distance = 14

        self.angle = 0
        self.speed = speed

        self.segments = []

        self.hitboxes = []

    def update(self):
        self.angle += self.speed
        self.segments.clear()
        self.hitboxes.clear()

        for i in range(1, self.length + 1):
            radius = i * self.segment_distance
            x = self.center_x + math.cos(self.angle) * radius
            y = self.center_y + math.sin(self.angle) * radius

            rect = pygame.Rect(
                x - self.segment_radius,
                y - self.segment_radius,
                self.segment_radius * 2,
                self.segment_radius * 2
            )
            self.segments.append(rect)
            self.hitboxes.append(rect)

    def draw(self, screen):
        for segment in self.segments:
            pygame.draw.circle(
                screen,
                (255, 80, 0),
                segment.center,
                self.segment_radius
            )

    def collides_with(self, player_rect):
        return any(player_rect.colliderect(seg) for seg in self.segments)
