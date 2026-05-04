import pygame
from persistence import load_leaderboard


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
DARK_GRAY = (80, 80, 80)


def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_button(screen, text, rect):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    font = pygame.font.SysFont("Arial", 28)
    label = font.render(text, True, BLACK)

    x = rect.x + (rect.width - label.get_width()) // 2
    y = rect.y + (rect.height - label.get_height()) // 2

    screen.blit(label, (x, y))


def input_name_screen(screen, clock):
    name = ""

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Enter your name:", 36, BLACK, 280, 200)
        draw_text(screen, name, 36, DARK_GRAY, 280, 270)
        draw_text(screen, "Press ENTER to start", 24, BLACK, 280, 340)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    name += event.unicode


def leaderboard_screen(screen, clock):
    back_button = pygame.Rect(330, 620, 180, 50)

    while True:
        screen.fill(WHITE)

        draw_text(screen, "TOP 10 LEADERBOARD", 36, BLACK, 230, 40)

        scores = load_leaderboard()

        y = 120
        for i, item in enumerate(scores, start=1):
            text = f"{i}. {item['name']} | Score: {item['score']} | Distance: {item['distance']} | Coins: {item['coins']}"
            draw_text(screen, text, 24, BLACK, 80, y)
            y += 40

        draw_button(screen, "Back", back_button)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "menu"


def settings_screen(screen, clock, settings):
    sound_button = pygame.Rect(280, 170, 280, 50)
    color_button = pygame.Rect(280, 250, 280, 50)
    difficulty_button = pygame.Rect(280, 330, 280, 50)
    back_button = pygame.Rect(330, 500, 180, 50)

    colors = ["red", "blue", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        draw_text(screen, "SETTINGS", 40, BLACK, 310, 70)

        draw_button(screen, f"Sound: {settings['sound']}", sound_button)
        draw_button(screen, f"Car: {settings['car_color']}", color_button)
        draw_button(screen, f"Difficulty: {settings['difficulty']}", difficulty_button)
        draw_button(screen, "Back", back_button)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                elif color_button.collidepoint(event.pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]

                elif difficulty_button.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]

                elif back_button.collidepoint(event.pos):
                    return "menu"


def game_over_screen(screen, clock, score, distance, coins):
    retry_button = pygame.Rect(280, 350, 280, 50)
    menu_button = pygame.Rect(280, 430, 280, 50)

    while True:
        screen.fill(WHITE)

        draw_text(screen, "GAME OVER", 48, BLACK, 270, 100)
        draw_text(screen, f"Score: {score}", 30, BLACK, 310, 190)
        draw_text(screen, f"Distance: {distance}", 30, BLACK, 310, 230)
        draw_text(screen, f"Coins: {coins}", 30, BLACK, 310, 270)

        draw_button(screen, "Retry", retry_button)
        draw_button(screen, "Main Menu", menu_button)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return "retry"

                if menu_button.collidepoint(event.pos):
                    return "menu"


def main_menu(screen, clock):
    play_button = pygame.Rect(300, 180, 240, 55)
    leader_button = pygame.Rect(300, 260, 240, 55)
    settings_button = pygame.Rect(300, 340, 240, 55)
    exit_button = pygame.Rect(300, 420, 240, 55)

    while True:
        screen.fill(WHITE)

        draw_text(screen, "TSIS3 RACER", 48, BLACK, 260, 80)

        draw_button(screen, "Play", play_button)
        draw_button(screen, "Leaderboard", leader_button)
        draw_button(screen, "Settings", settings_button)
        draw_button(screen, "Exit", exit_button)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return "play"

                if leader_button.collidepoint(event.pos):
                    return "leaderboard"

                if settings_button.collidepoint(event.pos):
                    return "settings"

                if exit_button.collidepoint(event.pos):
                    return "quit"