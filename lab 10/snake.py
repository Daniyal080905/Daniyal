import pygame
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Snake settings
snake = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"
next_direction = "RIGHT"

# Score, level, speed
score = 0
level = 1
speed = 8

# Food
food = [0, 0]


def generate_food():
    """Generate food not on wall and not on snake."""
    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)

        if [x, y] not in snake:
            return [x, y]


food = generate_food()


running = True
game_over = False

while running:
    clock.tick(speed)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Control snake direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                next_direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                next_direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                next_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                next_direction = "RIGHT"

    direction = next_direction

    # Move snake head
    head_x, head_y = snake[0]

    if direction == "UP":
        head_y -= CELL
    elif direction == "DOWN":
        head_y += CELL
    elif direction == "LEFT":
        head_x -= CELL
    elif direction == "RIGHT":
        head_x += CELL

    new_head = [head_x, head_y]

    # Wall collision check
    if (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT
    ):
        game_over = True

    # Self collision check
    if new_head in snake:
        game_over = True

    if game_over:
        print("Game Over!")
        running = False
        continue

    # Add new head
    snake.insert(0, new_head)

    # Food collision
    if new_head == food:
        score += 1

        # Every 4 foods, level increases
        if score % 4 == 0:
            level += 1
            speed += 2

        food = generate_food()
    else:
        # Remove tail if food not eaten
        snake.pop()

    # Draw background
    screen.fill(BLACK)

    # Draw snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Draw score and level
    text = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()