import pygame
import random
import time

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Advanced")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
YELLOW = (255, 220, 0)
PURPLE = (160, 60, 220)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Snake
snake = [[100, 100], [80, 100], [60, 100]]
direction = "RIGHT"
next_direction = "RIGHT"

# Score / level / speed
score = 0
level = 1
speed = 8

# Food settings
food = None
FOOD_LIFETIME = 5  # seconds


def generate_food():
    """Generate food with random weight, color and lifetime."""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        # Food must not appear on snake
        if [x, y] not in snake:
            break

    food_types = [
        {"weight": 1, "color": RED},
        {"weight": 2, "color": YELLOW},
        {"weight": 3, "color": PURPLE}
    ]

    food_type = random.choice(food_types)

    return {
        "pos": [x, y],
        "weight": food_type["weight"],
        "color": food_type["color"],
        "created_time": time.time()
    }


food = generate_food()

running = True

while running:
    clock.tick(speed)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard control
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

    # Move snake
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

    # Wall collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        print("Game Over: wall collision")
        running = False
        continue

    # Self collision
    if new_head in snake:
        print("Game Over: snake collision")
        running = False
        continue

    # Add new head
    snake.insert(0, new_head)

    # If food time is over, generate new food
    if time.time() - food["created_time"] > FOOD_LIFETIME:
        food = generate_food()

    # Food collision
    if new_head == food["pos"]:
        score += food["weight"]

        # Snake grows according to food weight
        for _ in range(food["weight"] - 1):
            snake.append(snake[-1])

        food = generate_food()

        # Level and speed increase every 5 score
        if score // 5 + 1 > level:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Draw
    screen.fill(BLACK)

    # Draw snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(
        screen,
        food["color"],
        (food["pos"][0], food["pos"][1], CELL, CELL)
    )

    # Timer
    time_left = max(0, FOOD_LIFETIME - int(time.time() - food["created_time"]))

    # Text
    text = font.render(
        f"Score: {score}   Level: {level}   Food: +{food['weight']}   Time: {time_left}",
        True,
        WHITE
    )
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()