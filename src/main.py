import pygame
import sys
import random

from maze import Maze
from player import Player
from enemy import FireBarEnemy
from timer import GameTimer
from settings import *
from leaderboard import save_score, load_scores
from gold import Gold

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
cell_px, cell_py = maze.maze_to_screen(0, 0)

player = Player(
    cell_px + (CELL_SIZE - PLAYER_SIZE) // 2,
    cell_py + (CELL_SIZE -PLAYER_SIZE) // 2 
)

enemy = FireBarEnemy(
    center_x = WIDTH // 2,
    center_y = UI_HEIGHT + HEIGHT // 2,
    length = 5,
    speed = 0.01
)

exit_rect = pygame.Rect(
    *maze.maze_to_screen(exit_x, exit_y),
    CELL_SIZE // 2,
    CELL_SIZE // 2
)

timer = GameTimer()
enemies = []
golds = []
gold_count = 0
gold_value = GOLD_VALUE
game_state = MENU
player_name = ""
score_saved = False
level = 1
final_score = 0

def draw_ui_banner():
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (0, 0, WIDTH, UI_HEIGHT)
    )

    pygame.draw.line(
        screen,
        (200, 200, 200),
        (0, UI_HEIGHT),
        (WIDTH, UI_HEIGHT),
        2
    )

    # Timer 
    time_text = small_font.render(
        f"Time: {timer.remaining()}s",
        True,
        (255, 255, 255)
    )
    screen.blit(time_text, (10, UI_HEIGHT // 2 - time_text.get_height() // 2))

    # Level anzeigen
    level_text = small_font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (10 + time_text.get_width() + 20, UI_HEIGHT // 2 - level_text.get_height() // 2))

    dash_radius = 10
    dash_x_offset = 20  
    dash_y = UI_HEIGHT // 2

    # Name und Position des Dash-Kreises links daneben
    name_text = small_font.render(player_name if player_name else "Player", True, (255, 255, 255))
    name_x = WIDTH // 2 - name_text.get_width() // 2

    dash_x = name_x - dash_radius * 2 - dash_x_offset 

    if player.dash_cooldown <= 0:
        # Dash bereit – voller grüner Kreis
        pygame.draw.circle(screen, (0, 255, 0), (dash_x, dash_y), dash_radius)
    else:
        # Dash im Cooldown – leerer Kreis mit rotem Rand
        pygame.draw.circle(screen, (255, 0, 0), (dash_x, dash_y), dash_radius, 2)

        # Füllung proportional zum Restcooldown
        fill_ratio = 1 - player.dash_cooldown / PLAYER_DASH_COOLDOWN
        fill_radius = int(dash_radius * fill_ratio)
        if fill_radius > 0:
            pygame.draw.circle(screen, (255, 0, 0), (dash_x, dash_y), fill_radius)

    # Spielername 
    screen.blit(
        name_text,
        (name_x, UI_HEIGHT // 2 - name_text.get_height() // 2)
    )

    # Gold 
    gold_text = small_font.render(f"Gold: {gold_count}", True, (255, 215, 0))
    gold_x = WIDTH - gold_text.get_width() - 10
    screen.blit(gold_text, (gold_x, UI_HEIGHT // 2 - gold_text.get_height() // 2))


def draw_maze():
    for x in range(COLS):
        for y in range(ROWS):
            cell = maze.grid[x][y]
            px, py = maze.maze_to_screen(x, y)

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
    
    draw_leaderboard(y_start=-40)

    draw_centered_text("Press R to Restart", small_font, (255, 255, 255), 160)
    draw_centered_text("Press ESC to Quit", small_font, (255, 255, 255), 200)


def draw_game_over_screen():
    screen.fill((120, 30, 30))
    draw_centered_text("GAME OVER", big_font, (255, 255, 255), -200)

    draw_leaderboard(y_start=-80)

    draw_centered_text("Press R to Restart", small_font, (255, 255, 255), 160)
    draw_centered_text("Press ESC to Quit", small_font, (255, 255, 255), 200)


def draw_leaderboard(y_start=40):
    scores = load_scores()

    title = small_font.render("Bestenliste", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 + y_start))

    for i, entry in enumerate(scores[:5]):
        color = (255, 215, 0) if i == 0 else (255, 255, 255)  # Gold für Platz 1

        display_name = entry["name"][:16]
        text = f"{i + 1}. {display_name} - {entry['Score']} Punkte"

        text = f"{i + 1}. {entry['name']} - {entry['Score']} Punkte"
        line = small_font.render(text, True, color)

        screen.blit(
            line,
            (
                WIDTH // 2 - line.get_width() // 2,
                HEIGHT // 2 + y_start + 30 + i * 30
            )
        )


def draw_main_menu():
    screen.fill((20, 20, 40))

    title = big_font.render("MAZE RUNNER", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

    prompt = small_font.render("Enter your name:", True, (200, 200, 200))
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 220))

    name = small_font.render(player_name + "|", True, (255, 255, 255))
    screen.blit(name, (WIDTH // 2 - name.get_width() // 2, 260))

    info1 = small_font.render("ENTER - Start Game", True, (180, 180, 180))
    info2 = small_font.render("L - Leaderboard", True, (180, 180, 180))
    info3 = small_font.render("ESC - Quit", True, (180, 180, 180))

    screen.blit(info1, (WIDTH // 2 - info1.get_width() // 2, 340))
    screen.blit(info2, (WIDTH // 2 - info2.get_width() // 2, 380))
    screen.blit(info3, (WIDTH // 2 - info3.get_width() // 2, 420))


def draw_leaderboard_screen():
    screen.fill((10, 10, 30))
    draw_centered_text("BESTENLISTE", big_font, (255, 255, 255), -200)
    draw_leaderboard(y_start=-120)

    hint = small_font.render("ESC - Back", True, (200, 200, 200))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 80))


def main():
    global game_state, player_name, score_saved, gold_count, level, final_score

    running = True
    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # -------- ESC --------
                if event.key == pygame.K_ESCAPE:
                    if game_state == MENU:
                        running = False
                    elif game_state == LEADERBOARD:
                        game_state = MENU
                    elif game_state in (GAME_OVER, WIN):
                        game_state = MENU
                    elif game_state == PLAYING:
                        running = False

                # -------- MENU --------
                if game_state == MENU:
                    if event.key == pygame.K_RETURN and player_name.strip():
                        restart_game()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_l:
                        game_state = LEADERBOARD
                    else:
                        if len(player_name) < 16 and event.unicode.isprintable():
                            player_name += event.unicode

                # -------- LEADERBOARD --------
                elif game_state == LEADERBOARD:
                    pass  # ESC wird oben behandelt

                # -------- GAME OVER / WIN --------
                elif game_state in (GAME_OVER, WIN):
                    if event.key == pygame.K_r:
                        level = 1
                        final_score = 0
                        restart_game()

            

        # GAME STATES
        if game_state == MENU:
            draw_main_menu()

        elif game_state == PLAYING:
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
            if keys[pygame.K_SPACE]:
                player.dash(walls)

            if dx != 0 and dy != 0:
                dx *= 0.7
                dy *= 0.7

            player.move(dx, dy, walls)

            for g in golds[:]:
                if player.rect.colliderect(g.rect):
                    golds.remove(g)
                    gold_count += 1

            player.update_cooldown()

            if player.rect.colliderect(exit_rect):
                final_score += timer.remaining()
                level += 1
                restart_game()

            if timer.remaining() <= 0:
                if not score_saved:
                    final_score += gold_count * gold_value
                    save_score(player_name, final_score)
                    score_saved = True
                game_state = GAME_OVER

            screen.fill(BG_COLOR)
            draw_ui_banner()
            draw_maze()
            pygame.draw.rect(screen, EXIT_COLOR, exit_rect)
            player.draw(screen)

            # Genger updaten und zeichnen
            for e in enemies: 
                e.update()
                e.draw(screen)
                if not player.dashing:
                    for hitbox in e.hitboxes:
                        if player.rect.colliderect(hitbox):
                            if not score_saved:
                                final_score += gold_count * gold_value
                                save_score(player_name, final_score)
                                score_saved = True
                            game_state = GAME_OVER

            for g in golds:
                g.draw(screen)

        elif game_state == WIN:
            draw_win_screen()

        elif game_state == GAME_OVER:
            draw_game_over_screen()

        elif game_state == LEADERBOARD:
            draw_leaderboard_screen()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def restart_game():
    global maze, walls, player, enemies, timer, game_state, exit_rect, player_name, score_saved, golds, gold_count, final_score

    golds = []
    gold_count = 0

    score_saved = False

    # Maze neu generieren
    maze.generate()
    exit_x, exit_y, _ = maze.create_exit()
    walls = maze.get_wall_rects()

    exit_rect = pygame.Rect(
        *maze.maze_to_screen(exit_x, exit_y),
        CELL_SIZE // 2,
        CELL_SIZE // 2
    )

    # Spielerposition zurücksetzen
    px, py = maze.maze_to_screen(0, 0)
    player.rect.topleft = (
        px + (CELL_SIZE - PLAYER_SIZE) // 2,
        py + (CELL_SIZE - PLAYER_SIZE) // 2 
    )

    # Gegnerliste erstellen
    enemies = []
    for _ in range(level):
        enemies.append(
            FireBarEnemy(
                center_x = random.randint(100, WIDTH - 100),
                center_y = random.randint(UI_HEIGHT + 100, HEIGHT - 100),
                length = 5 + (level - 1),
                speed = 0.01
            )
        )

    # Alle freien Zellen sammeln (Keine Wand, kein Spieler, kein Exit)
    free_cells = []
    for x in range(COLS):
        for y in range(ROWS):
            px, py = maze.maze_to_screen(x, y)
            cell_rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)
            if not any(cell_rect.colliderect(w) for w in walls) and \
                not cell_rect.colliderect(player.rect) and \
                not cell_rect.colliderect(exit_rect):
                free_cells.append((px, py))

    # Pro Feuerstange 1 Gold erzeugen
    for _ in range(level):
        if not free_cells:
            break
        px, py = random.choice(free_cells)
        free_cells.remove((px, py))
        golds.append(
            Gold(
                px + CELL_SIZE // 2,
                py + CELL_SIZE // 2
            )
        )

    timer = GameTimer()
    game_state = PLAYING



if __name__ == "__main__":
    main()



