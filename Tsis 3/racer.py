import pygame
import random
import time
from persistence import add_score


WIDTH = 840
HEIGHT = 700

ROAD_X = 170
ROAD_WIDTH = 500
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

FINISH_DISTANCE = 5000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD = (50, 50, 50)
YELLOW = (255, 220, 0)
RED = (220, 0, 0)
BLUE = (0, 80, 255)
GREEN = (0, 200, 0)
ORANGE = (255, 140, 0)
PURPLE = (150, 0, 200)
GRAY = (120, 120, 120)


def get_car_color(name):
    if name == "blue":
        return BLUE
    if name == "green":
        return GREEN
    if name == "yellow":
        return YELLOW
    return RED


class RacerGame:
    def __init__(self, screen, clock, player_name, settings):
        self.screen = screen
        self.clock = clock
        self.player_name = player_name
        self.settings = settings

        self.car_color = get_car_color(settings["car_color"])

        if settings["difficulty"] == "easy":
            self.base_speed = 5
            self.spawn_rate = 55
        elif settings["difficulty"] == "hard":
            self.base_speed = 8
            self.spawn_rate = 35
        else:
            self.base_speed = 6
            self.spawn_rate = 45

        self.player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 110, 50, 80)

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.road_events = []

        self.score = 0
        self.coins_count = 0
        self.distance = 0

        self.speed = self.base_speed
        self.frame = 0

        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.running = True
        self.game_over = False

    def lane_x(self, lane):
        return ROAD_X + lane * LANE_WIDTH + LANE_WIDTH // 2 - 25

    def safe_spawn_lane(self):
        player_lane = (self.player.centerx - ROAD_X) // LANE_WIDTH

        possible = []

        for lane in range(LANE_COUNT):
            if abs(lane - player_lane) > 0:
                possible.append(lane)

        if not possible:
            return random.randint(0, LANE_COUNT - 1)

        return random.choice(possible)

    def spawn_traffic(self):
        lane = self.safe_spawn_lane()
        car = pygame.Rect(self.lane_x(lane), -90, 50, 80)
        self.traffic.append(car)

    def spawn_obstacle(self):
        lane = self.safe_spawn_lane()
        kind = random.choice(["barrier", "oil", "pothole", "slow"])

        obstacle = {
            "rect": pygame.Rect(self.lane_x(lane), -60, 55, 40),
            "type": kind
        }

        self.obstacles.append(obstacle)

    def spawn_coin(self):
        lane = random.randint(0, LANE_COUNT - 1)
        value = random.choice([1, 2, 5])

        coin = {
            "rect": pygame.Rect(self.lane_x(lane) + 15, -40, 25, 25),
            "value": value
        }

        self.coins.append(coin)

    def spawn_powerup(self):
        lane = random.randint(0, LANE_COUNT - 1)
        kind = random.choice(["nitro", "shield", "repair"])

        powerup = {
            "rect": pygame.Rect(self.lane_x(lane), -40, 45, 45),
            "type": kind,
            "created": time.time()
        }

        self.powerups.append(powerup)

    def spawn_road_event(self):
        lane = random.randint(0, LANE_COUNT - 1)
        kind = random.choice(["moving_barrier", "speed_bump", "nitro_lane"])

        event = {
            "rect": pygame.Rect(self.lane_x(lane), -70, 70, 40),
            "type": kind,
            "direction": random.choice([-2, 2])
        }

        self.road_events.append(event)

    def activate_powerup(self, kind):
        if self.active_power is not None:
            return

        if kind == "nitro":
            self.active_power = "nitro"
            self.power_end_time = time.time() + 4
            self.speed += 4
            self.score += 20

        elif kind == "shield":
            self.active_power = "shield"
            self.shield = True
            self.score += 15

        elif kind == "repair":
            if self.obstacles:
                self.obstacles.pop(0)
            self.score += 10

    def update_powerup(self):
        if self.active_power == "nitro":
            if time.time() > self.power_end_time:
                self.speed = self.base_speed
                self.active_power = None

        if self.active_power == "shield":
            pass

    def handle_collision(self, rect):
        if self.shield:
            self.shield = False
            self.active_power = None
        else:
            self.game_over = True

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.player.left > ROAD_X:
            self.player.x -= 7

        if keys[pygame.K_RIGHT] and self.player.right < ROAD_X + ROAD_WIDTH:
            self.player.x += 7

        self.frame += 1
        self.distance += self.speed
        self.score = self.coins_count * 10 + self.distance // 10

        difficulty_bonus = self.distance // 1000
        current_spawn = max(18, self.spawn_rate - difficulty_bonus * 5)

        if self.frame % current_spawn == 0:
            self.spawn_traffic()

        if self.frame % 80 == 0:
            self.spawn_obstacle()

        if self.frame % 60 == 0:
            self.spawn_coin()

        if self.frame % 250 == 0:
            self.spawn_powerup()

        if self.frame % 180 == 0:
            self.spawn_road_event()

        for car in self.traffic[:]:
            car.y += self.speed + 2

            if car.colliderect(self.player):
                self.handle_collision(car)

            if car.top > HEIGHT:
                self.traffic.remove(car)

        for obstacle in self.obstacles[:]:
            obstacle["rect"].y += self.speed

            if obstacle["rect"].colliderect(self.player):
                if obstacle["type"] == "slow" or obstacle["type"] == "oil":
                    self.speed = max(3, self.speed - 2)
                    self.obstacles.remove(obstacle)
                else:
                    self.handle_collision(obstacle["rect"])

            elif obstacle["rect"].top > HEIGHT:
                self.obstacles.remove(obstacle)

        for coin in self.coins[:]:
            coin["rect"].y += self.speed

            if coin["rect"].colliderect(self.player):
                self.coins_count += coin["value"]
                self.score += coin["value"] * 10
                self.coins.remove(coin)

            elif coin["rect"].top > HEIGHT:
                self.coins.remove(coin)

        for powerup in self.powerups[:]:
            powerup["rect"].y += self.speed

            if time.time() - powerup["created"] > 7:
                self.powerups.remove(powerup)

            elif powerup["rect"].colliderect(self.player):
                self.activate_powerup(powerup["type"])
                self.powerups.remove(powerup)

        for event in self.road_events[:]:
            event["rect"].y += self.speed

            if event["type"] == "moving_barrier":
                event["rect"].x += event["direction"]

                if event["rect"].left < ROAD_X or event["rect"].right > ROAD_X + ROAD_WIDTH:
                    event["direction"] *= -1

            if event["rect"].colliderect(self.player):
                if event["type"] == "nitro_lane":
                    self.activate_powerup("nitro")
                elif event["type"] == "speed_bump":
                    self.speed = max(3, self.speed - 1)
                else:
                    self.handle_collision(event["rect"])

            if event["rect"].top > HEIGHT:
                self.road_events.remove(event)

        self.update_powerup()

        if self.distance >= FINISH_DISTANCE:
            self.game_over = True

    def draw_road(self):
        pygame.draw.rect(self.screen, ROAD, (ROAD_X, 0, ROAD_WIDTH, HEIGHT))

        for i in range(1, LANE_COUNT):
            x = ROAD_X + i * LANE_WIDTH
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT), 4)

        pygame.draw.rect(self.screen, GREEN, (0, 0, ROAD_X, HEIGHT))
        pygame.draw.rect(self.screen, GREEN, (ROAD_X + ROAD_WIDTH, 0, WIDTH - ROAD_X - ROAD_WIDTH, HEIGHT))

    def draw_objects(self):
        pygame.draw.rect(self.screen, self.car_color, self.player)
        pygame.draw.rect(self.screen, BLACK, self.player, 2)

        for car in self.traffic:
            pygame.draw.rect(self.screen, BLUE, car)
            pygame.draw.rect(self.screen, BLACK, car, 2)

        for obstacle in self.obstacles:
            rect = obstacle["rect"]

            if obstacle["type"] == "barrier":
                color = ORANGE
            elif obstacle["type"] == "oil":
                color = BLACK
            elif obstacle["type"] == "pothole":
                color = GRAY
            else:
                color = PURPLE

            pygame.draw.rect(self.screen, color, rect)

        for coin in self.coins:
            pygame.draw.circle(self.screen, YELLOW, coin["rect"].center, 13)
            font = pygame.font.SysFont("Arial", 18)
            text = font.render(str(coin["value"]), True, BLACK)
            self.screen.blit(text, (coin["rect"].x + 7, coin["rect"].y + 3))

        for powerup in self.powerups:
            rect = powerup["rect"]

            if powerup["type"] == "nitro":
                color = ORANGE
                label = "N"
            elif powerup["type"] == "shield":
                color = BLUE
                label = "S"
            else:
                color = GREEN
                label = "R"

            pygame.draw.rect(self.screen, color, rect)
            font = pygame.font.SysFont("Arial", 24)
            text = font.render(label, True, WHITE)
            self.screen.blit(text, (rect.x + 14, rect.y + 8))

        for event in self.road_events:
            rect = event["rect"]

            if event["type"] == "moving_barrier":
                color = RED
            elif event["type"] == "speed_bump":
                color = ORANGE
            else:
                color = GREEN

            pygame.draw.rect(self.screen, color, rect)

    def draw_ui(self):
        font = pygame.font.SysFont("Arial", 24)

        remaining = max(0, FINISH_DISTANCE - self.distance)

        lines = [
            f"Player: {self.player_name}",
            f"Score: {self.score}",
            f"Coins: {self.coins_count}",
            f"Distance: {self.distance}/{FINISH_DISTANCE}",
            f"Remaining: {remaining}",
            f"Power: {self.active_power}"
        ]

        y = 20

        for line in lines:
            text = font.render(line, True, BLACK)
            self.screen.blit(text, (10, y))
            y += 30

        pygame.draw.rect(self.screen, BLACK, (10, 210, 140, 20), 2)
        progress = min(140, int((self.distance / FINISH_DISTANCE) * 140))
        pygame.draw.rect(self.screen, GREEN, (10, 210, progress, 20))

        if self.active_power == "nitro":
            left = max(0, int(self.power_end_time - time.time()))
            text = font.render(f"Nitro time: {left}s", True, BLACK)
            self.screen.blit(text, (10, 240))

        if self.shield:
            text = font.render("Shield: active", True, BLACK)
            self.screen.blit(text, (10, 270))

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_road()
        self.draw_objects()
        self.draw_ui()
        pygame.display.flip()

    def run(self):
        while self.running and not self.game_over:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            self.update()
            self.draw()

        add_score(self.player_name, self.score, self.distance, self.coins_count)

        return {
            "score": self.score,
            "distance": self.distance,
            "coins": self.coins_count
        }