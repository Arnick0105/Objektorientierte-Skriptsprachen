import random
import pygame
from settings import CELL_SIZE

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True
        }
        self.visited = False


class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid = [[Cell(x, y) for y in range(rows)] for x in range(cols)]

    def get_neighbors(self, cell):
        neighbors = []

        directions = {
            "top": (0, -1),
            "right": (1, 0),
            "bottom": (0, 1),
            "left": (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                neighbor = self.grid[nx][ny]
                if not neighbor.visited:
                    neighbors.append((direction, neighbor))

        return neighbors

    def remove_walls(self, current, direction, next_cell):
        if direction == "top":
            current.walls["top"] = False
            next_cell.walls["bottom"] = False
        elif direction == "right":
            current.walls["right"] = False
            next_cell.walls["left"] = False
        elif direction == "bottom":
            current.walls["bottom"] = False
            next_cell.walls["top"] = False
        elif direction == "left":
            current.walls["left"] = False
            next_cell.walls["right"] = False

    def generate(self):
        stack = []
        current = self.grid[0][0]
        current.visited = True

        while True:
            neighbors = self.get_neighbors(current)

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.remove_walls(current, direction, next_cell)
                stack.append(current)
                current = next_cell
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                break

    def get_wall_rects(self):
        walls = []
        thickness = 4

        for x in range(self.cols):
            for y in range(self.rows):
                cell = self.grid[x][y]
                px, py = x * CELL_SIZE, y * CELL_SIZE

                if cell.walls["top"]:
                    walls.append(pygame.Rect(px, py, CELL_SIZE, thickness))
                if cell.walls["right"]:
                    walls.append(pygame.Rect(px + CELL_SIZE - thickness, py, thickness, CELL_SIZE))
                if cell.walls["bottom"]:
                    walls.append(pygame.Rect(px, py + CELL_SIZE - thickness, CELL_SIZE, thickness))
                if cell.walls["left"]:
                    walls.append(pygame.Rect(px, py, thickness, CELL_SIZE))

        return walls
