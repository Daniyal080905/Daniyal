import pygame
import random

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player car
car_width = 50
car_height = 90
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 6

# Enemy car
enemy_width = 50
enemy_height = 90
enemy_x = random.randint(60, WIDTH - 110)
enemy_y = -100
enemy_speed = 5

# Coin
coin_radius = 15
coin_x = random.randint(60, WIDTH - 60)
coin_y = -50
coin_speed = 4
coins = 0

# Font
font = pygame.font.SysFont("Arial", 28)


def draw_road():
    # Draw road background
    screen.fill(GRAY)

    # Draw side lines
    pygame.draw.rect(screen, WHITE, (40, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 45, 0, 5, HEIGHT))

    # Draw center line
    for y in range(0, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 40))


def draw_player(x, y):
    # Draw player car
    pygame.draw.rect(screen, BLUE, (x, y, car_width, car_height))
    pygame.draw.rect(screen, BLACK, (x + 10, y + 10, 30, 20))


def draw_enemy(x, y):
    # Draw enemy car
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height))
    pygame.draw.rect(screen, BLACK, (x + 10, y + 10, 30, 20))


def draw_coin(x, y):
    # Draw coin
    pygame.draw.circle(screen, YELLOW, (x, y), coin_radius)
    pygame.draw.circle(screen, BLACK, (x, y), coin_radius, 2)


def show_score():
    # Show collected coins in top right corner
    text = font.render(f"Coins: {coins}", True, WHITE)
    screen.blit(text, (WIDTH - 130, 10))


running = True

while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard control
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

    # Coin movement
    coin_y += coin_speed

    if coin_y > HEIGHT:
        coin_y = -50
        coin_x = random.randint(60, WIDTH - 60)

    # Rectangles for collision
    player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    coin_rect = pygame.Rect(
        coin_x - coin_radius,
        coin_y - coin_radius,
        coin_radius * 2,
        coin_radius * 2
    )

    # Collision with enemy
    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        running = False

    # Collision with coin
    if player_rect.colliderect(coin_rect):
        coins += 1
        coin_y = -50
        coin_x = random.randint(60, WIDTH - 60)

    # Draw everything
    draw_road()
    draw_player(car_x, car_y)
    draw_enemy(enemy_x, enemy_y)
    draw_coin(coin_x, coin_y)
    show_score()

    pygame.display.update()

pygame.quit()