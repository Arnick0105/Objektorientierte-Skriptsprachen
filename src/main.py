import pygame
import sys

from maze import Maze
from player import Player
from enemy import Enemy
from timer import GameTimer
from settings import *
from leaderboard import save_score, load_scores

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()
big_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

maze = Maze(COLS, ROWS)
maze.generate()
exit_x, exit_y, exit_wall = maze.create_exit()
walls = maze.get_wall_rects()

player = Player(
    CELL_SIZE * 0 + CELL_SIZE // 4,
    CELL_SIZE * 0 + CELL_SIZE // 4
)

enemy = Enemy(
    WIDTH - CELL_SIZE,
    HEIGHT - CELL_SIZE
)

exit_rect = pygame.Rect(
    exit_x * CELL_SIZE + CELL_SIZE // 4,
    exit_y * CELL_SIZE + CELL_SIZE // 4,
    CELL_SIZE // 2,
    CELL_SIZE // 2
)

timer = GameTimer()
game_state = PLAYING
player_name = ""
entering_name = False
score_saved = False


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


def draw_centered_text(text, font, color, y_offset=0):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)


def draw_win_screen():
    screen.fill((20, 80, 20))
    draw_centered_text("YOU WIN!", big_font, (255, 255, 255), -160)

    if entering_name:
        draw_name_input()
    else:
        draw_leaderboard(y_start=-40)

        draw_centered_text("Press R to Restart", small_font, (255, 255, 255), 160)
        draw_centered_text("Press ESC to Quit", small_font, (255, 255, 255), 200)


def draw_game_over_screen():
    screen.fill((120, 30, 30))
    draw_centered_text("GAME OVER", big_font, (255, 255, 255), -40)
    draw_centered_text("Press R to Restart", small_font, (255, 255, 255), 20)
    draw_centered_text("Press ESC to Quit", small_font, (255, 255, 255), 60)


def draw_leaderboard(y_start=40):
    scores = load_scores()

    title = small_font.render("Bestenliste", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 + y_start))

    for i, entry in enumerate(scores[:5]):
        color = (255, 215, 0) if i == 0 else (255, 255, 255)  # Gold für Platz 1

        display_name = entry["name"][:16]
        text = f"{i + 1}. {display_name} - {entry['time']}s"

        text = f"{i + 1}. {entry['name']} - {entry['time']}s"
        line = small_font.render(text, True, color)

        screen.blit(
            line,
            (
                WIDTH // 2 - line.get_width() // 2,
                HEIGHT // 2 + y_start + 30 + i * 30
            )
        )


def draw_name_input():
    prompt = small_font.render("Enter your name:", True, (255, 255, 255))
    name = small_font.render(player_name + "|", True, (255, 255, 255))

    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(name, (WIDTH // 2 - name.get_width() // 2, HEIGHT // 2 + 20))


def main():
    global game_state

    running = True
    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r and game_state != PLAYING:
                    restart_game()
                
                if game_state == WIN and entering_name:

                    if event.key == pygame.K_RETURN and player_name.strip():
                        save_score(player_name.strip(), max(0, timer.remaining()))
                        entering_name = False

                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]

                    else:
                        if len(player_name) < 16 and event.unicode.isprintable():
                            player_name += event.unicode

            

        # GAME STATES
        if game_state == PLAYING:
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

            if dx != 0 and dy != 0:
                dx *= 0.7
                dy *= 0.7

            player.move(dx, dy, walls)
            enemy.update(walls)

            if player.rect.colliderect(enemy.rect):
                game_state = GAME_OVER

            if player.rect.colliderect(exit_rect):
                entering_name = True
                score_saved = False
                game_state = WIN

            if timer.remaining() <= 0:
                game_state = GAME_OVER

            screen.fill(BG_COLOR)
            draw_maze()
            pygame.draw.rect(screen, EXIT_COLOR, exit_rect)
            player.draw(screen)
            enemy.draw(screen)

            time_text = small_font.render(
                f"Time: {timer.remaining()}",
                True,
                (255, 255, 255)
            )
            screen.blit(time_text, (10, 10))

        elif game_state == WIN:
            draw_win_screen()

        elif game_state == GAME_OVER:
            draw_game_over_screen()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def restart_game():
    global maze, walls, player, enemy, timer
    global game_state, exit_rect, player_name, entering_name, score_saved

    maze.generate()
    exit_x, exit_y, _ = maze.create_exit()
    walls = maze.get_wall_rects()

    exit_rect = pygame.Rect(
        exit_x * CELL_SIZE + CELL_SIZE // 4,
        exit_y * CELL_SIZE + CELL_SIZE // 4,
        CELL_SIZE // 2,
        CELL_SIZE // 2
    )

    player.rect.topleft = (CELL_SIZE // 4, CELL_SIZE // 4)
    enemy.rect.topleft = (WIDTH - CELL_SIZE, HEIGHT - CELL_SIZE)

    player_name = ""
    entering_name = False
    score_saved = False

    timer = GameTimer()
    game_state = PLAYING



if __name__ == "__main__":
    main()













# Dash zum ausweichen von "Gegnern" (drehende Feuerstangen)
# Player kann manchmal nicht an Wänden vorbei weil die Bewegeung nicht kleine Schritte zulässt
# Münzen oder anderes zum aufsammeln (vielleicht mehr Zeit dadurch oder separate Punkte oder kombination aus Restzeit und Münzen)