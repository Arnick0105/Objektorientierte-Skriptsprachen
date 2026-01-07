import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.dash_cooldown = 0
        self.dashing = False
        self.dash_distance = PLAYER_DASH_DISTANCE
        self.last_dx = 1 # Default: nach rechts
        self.last_dy = 0


    def dash (self, walls):
        if self.dash_cooldown > 0:
            return
        
        self.dashing = True
        self.dash_cooldown = PLAYER_DASH_COOLDOWN

        dash_steps = int(self.dash_distance)
        step_x = self.last_dx
        step_y = self.last_dy

        for _ in range (dash_steps):
            self.rect.x += step_x
            if any(self.rect.colliderect(w) for w in walls):
                if step_x > 0:
                    self.rect.right = min(w.left for w in walls if self.rect.colliderect(w))
                elif step_x < 0:
                    self.rect.left = max(w.right for w in walls if self.rect.colliderect(w))
                break

            self.rect.y += step_y
            if any(self.rect.colliderect(w) for w in walls):
                if step_y > 0:
                    self.rect.bottom = min(w.top for w in walls if self.rect.colliderect(w))
                elif step_y < 0:
                    self.rect.top = max(w.bottom for w in walls if self.rect.colliderect(w))
                break

        self.dashing = False


    def update_cooldown(self):
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1


    def move(self, dx, dy, walls):
        steps = int(max(abs(dx), abs(dy)) * self.speed)

        if dx != 0 or dy != 0:
            self.last_dx = dx
            self.last_dy = dy

        if steps == 0:
            return

        step_x = (dx * self.speed) / steps
        step_y = (dy * self.speed) / steps

        for _ in range(steps):
            # X-Achse
            self.rect.x += step_x
            for wall in walls:
                if self.rect.colliderect(wall):
                    if step_x > 0:
                        self.rect.right = wall.left
                    elif step_x < 0:
                        self.rect.left = wall.right

            # Y-Achse
            self.rect.y += step_y
            for wall in walls:
                if self.rect.colliderect(wall):
                    if step_y > 0:
                        self.rect.bottom = wall.top
                    elif step_y < 0:
                        self.rect.top = wall.bottom


    def draw(self, screen):
        # Spieler-Rechteck
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)

        center_x, center_y = self.rect.center

        arrow_length = PLAYER_SIZE // 2 + 6
        end_x = center_x + self.last_dx * arrow_length
        end_y = center_y + self.last_dy * arrow_length

        #Linie für Blickrichtung
        pygame.draw.line(screen, (226, 0, 116), (center_x, center_y), (end_x, end_y), 3)

        tip_size = 4
        if self.last_dx != 0 or self.last_dy != 0:
            
            perp_x = -self.last_dy * tip_size
            perp_y = self.last_dx * tip_size

            pygame.draw.line(screen, (226, 0, 116), (end_x, end_y), (end_x - self.last_dx * tip_size + perp_x, end_y - self.last_dy * tip_size + perp_y), 3)
            pygame.draw.line(screen, (226, 0, 116), (end_x, end_y), (end_x - self.last_dx * tip_size - perp_x, end_y - self.last_dy * tip_size - perp_y), 3)
