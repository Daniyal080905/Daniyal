import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Advanced")

# Colors
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
GOLD = (255, 165, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

# Player
car_width, car_height = 50, 90
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - 120
car_speed = 6

# Enemy
enemy_width, enemy_height = 50, 90
enemy_x = random.randint(60, WIDTH - 110)
enemy_y = -100
enemy_speed = 5

# Coins list (могут быть разные)
coins = []

# Score
score = 0

# Font
font = pygame.font.SysFont("Arial", 24)


def draw_road():
    """Draw road"""
    screen.fill(GRAY)

    pygame.draw.rect(screen, WHITE, (40, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 45, 0, 5, HEIGHT))

    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 40))


def draw_player():
    """Draw player car"""
    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))


def draw_enemy():
    """Draw enemy car"""
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))


def spawn_coin():
    """Создаём монету со случайным весом"""
    coin_type = random.choice([
        {"value": 1, "color": YELLOW, "radius": 10},
        {"value": 3, "color": GOLD, "radius": 14}
    ])

    x = random.randint(60, WIDTH - 60)
    y = -20

    coins.append({
        "x": x,
        "y": y,
        "value": coin_type["value"],
        "color": coin_type["color"],
        "radius": coin_type["radius"]
    })


def draw_coins():
    """Draw all coins"""
    for coin in coins:
        pygame.draw.circle(screen, coin["color"], (coin["x"], coin["y"]), coin["radius"])


def move_coins():
    """Move coins down"""
    for coin in coins:
        coin["y"] += 4


def check_coin_collision():
    """Check if player collects coins"""
    global score

    player_rect = pygame.Rect(car_x, car_y, car_width, car_height)

    for coin in coins[:]:
        coin_rect = pygame.Rect(
            coin["x"] - coin["radius"],
            coin["y"] - coin["radius"],
            coin["radius"] * 2,
            coin["radius"] * 2
        )

        if player_rect.colliderect(coin_rect):
            score += coin["value"]  # добавляем вес монеты
            coins.remove(coin)


def show_score():
    """Show score"""
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and car_x > 50:
        car_x -= car_speed

    if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width - 50:
        car_x += car_speed

    # Enemy movement
    enemy_y += enemy_speed

    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(60, WIDTH - enemy_width - 60)

    # Increase difficulty (каждые 10 очков ускорение)
    enemy_speed = 5 + score // 10

    # Spawn coins randomly
    if random.randint(1, 60) == 1:
        spawn_coin()

    move_coins()
    check_coin_collision()

    # Collision with enemy
    player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

    if player_rect.colliderect(enemy_rect):
        print("Game Over")
        running = False

    # Draw
    draw_road()
    draw_player()
    draw_enemy()
    draw_coins()
    show_score()

    pygame.display.update()

pygame.quit()