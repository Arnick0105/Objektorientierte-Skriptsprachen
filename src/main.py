import pygame
import sys

from maze import Maze
from player import Player
from enemy import Enemy
from timer import GameTimer
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

maze = Maze(COLS, ROWS)
maze.generate()
walls = maze.get_wall_rects()

player = Player(
    CELL_SIZE * 0 + CELL_SIZE // 4,
    CELL_SIZE * 0 + CELL_SIZE // 4
)
enemy = Enemy(
    WIDTH - CELL_SIZE,
    HEIGHT - CELL_SIZE
)

exit_rect = pygame.Rect(WIDTH - CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE, CELL_SIZE)
timer = GameTimer()

def draw_maze():
    for x in range(COLS):
        for y in range(ROWS):
            cell = maze.grid[x][y]
            px, py = x * CELL_SIZE, y * CELL_SIZE

            if cell.walls["top"]:
                pygame.draw.line(screen, WALL_COLOR, (px, py), (px + CELL_SIZE, py))
            if cell.walls["right"]:
                pygame.draw.line(screen, WALL_COLOR, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE))
            if cell.walls["bottom"]:
                pygame.draw.line(screen, WALL_COLOR, (px, py + CELL_SIZE), (px + CELL_SIZE, py + CELL_SIZE))
            if cell.walls["left"]:
                pygame.draw.line(screen, WALL_COLOR, (px, py), (px, py + CELL_SIZE))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = 1

        player.move(dx, dy, walls)
        enemy.update(walls)

        if player.rect.colliderect(enemy.rect):
            print("GAME OVER – Gegner erwischt!")
            running = False

        if player.rect.colliderect(exit_rect):
            print("GEWONNEN! 🎉")
            running = False

        if timer.remaining() <= 0:
            print("ZEIT ABGELAUFEN ⏱️")
            running = False

        screen.fill(BG_COLOR)
        draw_maze()

        pygame.draw.rect(screen, EXIT_COLOR, exit_rect)
        player.draw(screen)
        enemy.draw(screen)

        time_text = font.render(f"Time: {timer.remaining()}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
